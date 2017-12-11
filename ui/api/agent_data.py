from game_data import get_client, get_db_handle
import bson


def get_agents(owner, db_handle=None):
    if db_handle is None:
        db_handle = get_db_handle("agents")
    collection = db_handle.agents
    result = collection.find({"owner": owner})
    return list(result)


def insert_new_agent(owner, name, game_type, db_handle):
    collection = db_handle.agents
    doc = {"owner": owner, "name": name, "game_type": game_type}
    agent_id = collection.insert_one(doc).inserted_id
    return agent_id


def get_agent_id(owner, name, game_type, db_handle=None):
    if db_handle is None:
        db_handle = get_db_handle("agents")
    if "agents" not in db_handle.collection_names():
        agent_id = insert_new_agent(owner, name, game_type, db_handle)
    else:
        collection = db_handle.agents
        result = list(collection.find({"owner": owner, "name": name, "game_type": game_type}))
        if len(result) > 0:
            agent_id = result[0]["_id"]
        else:
            agent_id = insert_new_agent(owner, name, game_type, db_handle)
    return agent_id


def save_agent_data(agent_id, data, key, db_handle=None):
    if db_handle is None:
        db_handle = get_db_handle("agents")

    if not isinstance(agent_id, bson.ObjectId):
        agent_id = bson.ObjectId(str(agent_id))

    collection = db_handle.agents
    update_spec = {"$set": {key: data}}
    data_id = collection.update_one({"_id": agent_id}, update_spec)


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


def save_game_result(agent_id, game_id, game_type, score, win, db_handle=None):
    if db_handle is None:
        db_handle = get_db_handle("agents")
    collection = db_handle.agents

    if not isinstance(agent_id, bson.ObjectId):
        agent_id = bson.ObjectId(str(agent_id))

    result = list(collection.find({"_id": agent_id}))
    if len(result) > 0:
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


def load_game_results(game_type, db_handle=None):
    if db_handle is None:
        db_handle = get_db_handle("agents")
    collection = db_handle.agents
    result = list(collection.find({"game_type": game_type}))

    stats = []

    for agent in result:
        if "results" in agent:
            stats.append((agent["owner"],
                          agent["name"],
                          agent["results"]["num_wins"] / agent["results"]["num_games"]))

    return stats
