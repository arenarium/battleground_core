from .game_data import get_db_handle
from battleground.utils import bg_trueskill
import bson


def get_agents(owner=None,
               game_type=None,
               agent_id=None,
               has_file=False,
               fields=None,
               db_handle=None):
    """
    get agent data for conditions:
    owner == owner
    game_type == game_type

    has_file: if True, only return records that have code_string

    fields:
    only return these field from the database

    db_handle: used for testing
    """

    if db_handle is None:
        db_handle = get_db_handle("agents")

    collection = db_handle.agents

    query = {}
    if agent_id is not None:
        if not isinstance(agent_id, bson.ObjectId):
            agent_id = bson.ObjectId(str(agent_id))
        query['_id'] = agent_id
    else:
        if owner is not None:
            query['owner'] = owner
        if game_type is not None:
            query['game_type'] = game_type
        if has_file:
            query['code'] = {'$exists': True, '$ne': 'null'}

    if fields is None:
        projection = {'_id': True, 'game_type': True, 'owner': True, 'name': True}
    else:
        projection = {field: True for field in fields}

    result = collection.find(query, projection=projection)
    return list(result)


def insert_new_agent(owner, name, game_type, db_handle):
    collection = db_handle.agents
    doc = {"owner": owner, "name": name, "game_type": game_type}
    agent_id = collection.insert_one(doc).inserted_id
    return agent_id


def get_owners(db_handle=None):
    if db_handle is None:
        db_handle = get_db_handle("agents")

    owners = set()

    collection = db_handle.agents
    for document in collection.find():
        owners.add(document["owner"])

    return owners


def get_agent_id(owner, name, game_type, db_handle=None):
    if db_handle is None:
        db_handle = get_db_handle("agents")

    if "agents" not in db_handle.collection_names():
        agent_id = insert_new_agent(owner, name, game_type, db_handle)
    else:
        collection = db_handle.agents
        result = list(collection.find({"owner": owner,
                                       "name": name,
                                       "game_type": game_type}))
        if result:
            agent_id = result[0]["_id"]
        else:
            agent_id = insert_new_agent(owner, name, game_type, db_handle)
    return agent_id


def save_agent_code(owner, name, game_type, code, db_handle=None):
    agent_id = get_agent_id(owner, name, game_type, db_handle=db_handle)
    save_agent_data(agent_id, data=code, key="code", db_handle=db_handle)
    return agent_id


def load_agent_code(owner, name, game_type, db_handle=None):
    agent_id = get_agent_id(owner, name, game_type, db_handle=db_handle)
    code = load_agent_data(agent_id, key="code", db_handle=db_handle)
    return code


def save_agent_data(agent_id, data, key, db_handle=None):
    if db_handle is None:
        db_handle = get_db_handle("agents")

    if not isinstance(agent_id, bson.ObjectId):
        agent_id = bson.ObjectId(str(agent_id))

    collection = db_handle.agents
    update_spec = {"$set": {key: data}}
    data_id = collection.update_one({"_id": agent_id}, update_spec)
    return data_id


def load_agent_data(agent_id, key, db_handle=None):
    if db_handle is None:
        db_handle = get_db_handle("agents")

    if not isinstance(agent_id, bson.ObjectId):
        agent_id = bson.ObjectId(str(agent_id))

    collection = db_handle.agents
    doc = collection.find_one(agent_id)
    if doc is not None:
        if key in doc:
            return doc[key]
    return None


def save_game_result(agent_ids,
                     game_id,
                     game_type,
                     scores,
                     time,
                     db_handle=None):
    if db_handle is None:
        db_handle = get_db_handle("agents")
    collection_a = db_handle.agents
    collection_r = db_handle.results

    # save results and get agents
    agents = []
    for index, agent_id in enumerate(agent_ids):
        # save to results table (used to search results by player/agent)
        score = scores[index]
        win = max(scores) == score and min(scores) != score
        result = {
            'agent_id': str(agent_id),
            'game_id': str(game_id),
            'game_type': game_type,
            'score': score,
            'win': win,
            'time': time
        }
        collection_r.save(result)

        # get agents
        if not isinstance(agent_id, bson.ObjectId):
            agent_id = bson.ObjectId(str(agent_id))
        agent_db_entry = list(collection_a.find({"_id": agent_id}))
        if agent_db_entry:
            agent = agent_db_entry[0]
        else:
            raise Exception("agent not found: {}".format(agent_id))
        agents.append(agent)

    agents = update_ratings(agents, scores)

    # save agents
    for agent in agents:
        collection_a.save(agent)


def update_ratings(agents, scores):
    """
    A ranking system based on TrueSkill(TM)
    :param agents: list of DB agents
    :param scores: list of scores
    :return: updated list of DB agents
    """
    # get ratings or initialize new ones in a free-for-all
    ratings = []
    for agent in agents:
        if "results" in agents:
            ratings.append((bg_trueskill.Rating(**agent["results"]["rating"]),))
        else:
            ratings.append((bg_trueskill.Rating(),))
    # lower rank is better
    ranks = [(0,) if score else (1,) for score in scores]
    new_ratings = bg_trueskill.rate(ratings, ranks=ranks, scores=scores)

    for index, agent in enumerate(agents):
        score = scores[index]
        win = max(scores) == score and min(scores) != score
        rank = bg_trueskill.expose(new_ratings[index][0])
        rating = {"mu": new_ratings[index][0].mu,
                  "sigma": new_ratings[index][0].sigma}
        if "results" in agent:
            num_games = agent["results"]["num_games"]
            avg_score = agent["results"]["avg_score"]
            agent["results"]["num_games"] += 1
            agent["results"]["avg_score"] = (avg_score * num_games + score) / (num_games + 1)
            agent["results"]["rank"] = rank
            agent["results"]["rating"] = rating
            if win:
                agent["results"]["num_wins"] += 1
        else:
            agent["results"] = {}
            agent["results"]["num_games"] = 1
            agent["results"]["avg_score"] = score
            agent["results"]["rank"] = rank
            agent["results"]["rating"] = rating
            agent["results"]["num_wins"] = 1 if win else 0
    return agents


def load_agent_results(agent_id, limit=10, db_handle=None):
    if db_handle is None:
        db_handle = get_db_handle("agents")
    collection = db_handle.results

    result = collection.find({"agent_id": str(agent_id)})
    result = result.sort("time", -1).limit(limit)
    return list(result)


def load_game_results(game_type, db_handle=None):
    if db_handle is None:
        db_handle = get_db_handle("agents")
    collection = db_handle.agents
    result = list(collection.find({"game_type": game_type}))

    stats = []

    for agent in result:
        if "results" in agent:
            # win_rate = agent["results"]["num_wins"] / agent["results"]["num_games"]
            rank = agent["results"]["rank"]
            stats.append((str(agent["_id"]), agent["owner"], agent["name"], rank))
    sorted_stats = sorted(stats, key=lambda x: x[-1], reverse=True)
    return sorted_stats
