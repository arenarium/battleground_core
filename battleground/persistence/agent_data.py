from .game_data import get_db_handle
import bson


def get_agents(owner=None, game_type=None, agent_id=None, has_file=False, fields=None, db_handle=None):
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


def save_game_result(agent_id,
                     game_id,
                     game_type,
                     score,
                     win,
                     time,
                     db_handle=None):
    if db_handle is None:
        db_handle = get_db_handle("agents")
    collection = db_handle.agents

    if not isinstance(agent_id, bson.ObjectId):
        agent_id = bson.ObjectId(str(agent_id))

    result = list(collection.find({"_id": agent_id}))
    if result:
        agent = result[0]
    else:
        raise Exception("agent not found: {}".format(agent_id))

    if "results" in agent:
        num_games = agent["results"]["num_games"]
        avg_score = agent["results"]["avg_score"]
        agent["results"]["num_games"] += 1
        agent["results"]["avg_score"] = (avg_score * num_games + score) / (num_games + 1)
        if win:
            agent["results"]["num_wins"] += 1
    else:
        agent["results"] = {}
        agent["results"]["num_games"] = 1
        agent["results"]["avg_score"] = score
        agent["results"]["num_wins"] = 1 if win else 0

    collection.save(agent)

    # now save to results table (used to search results by player/agent)
    collection = db_handle.results

    result = {
        'agent_id': str(agent_id),
        'game_id': str(game_id),
        'game_type': game_type,
        'score': score,
        'win': win,
        'time': time
    }
    collection.save(result)


def load_agent_results(agent_id, limit=10, db_handle=None):
    if db_handle is None:
        db_handle = get_db_handle("agents")
    collection = db_handle.results

    result = collection.find({"agent_id": str(agent_id)})
    result = result.sort('time', -1).limit(limit)
    return list(result)


def load_game_results(game_type, db_handle=None):
    if db_handle is None:
        db_handle = get_db_handle("agents")
    collection = db_handle.agents
    result = list(collection.find({"game_type": game_type}))

    stats = []

    for agent in result:
        if "results" in agent:
            win_rate = agent["results"]["num_wins"] / agent["results"]["num_games"]
            stats.append((str(agent['_id']), agent["owner"], agent["name"], win_rate))
    sorted_stats = sorted(stats, key=lambda x: x[-1], reverse=True)
    return sorted_stats
