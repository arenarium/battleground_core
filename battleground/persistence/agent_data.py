from .game_data import get_client, get_db_handle


def get_agents(owner,db_handle=None):
    if db_handle is None:
        db_handle = get_db_handle("agents")
    collection = db_handle.agents
    result = collection.find({"owner": owner})
    return list(result)

def insert_new_agent(owner, name, game_type, db_handle):
    collection = db_handle.agents
    doc = {"owner": owner, "name": name,"game_type":game_type}
    agent_id = collection.insert_one(doc).inserted_id
    return agent_id


def get_agent_id(owner, name, game_type, db_handle=None):
    if db_handle is None:
        db_handle = get_db_handle("agents")
    if "agents" not in db_handle.collection_names():
        agent_id = insert_new_agent(owner, name, game_type, db_handle)
    else:
        collection = db_handle.agents
        result = list(collection.find({"owner": owner, "name": name,"game_type":game_type}))
        if len(result)>0:
            agent_id =  result[0]["_id"]
        else:
            agent_id = insert_new_agent(owner, name, game_type, db_handle)
    return agent_id


def save_agent_data(agent_id, data, db_handle=None):
    if db_handle is None:
        db_handle = get_db_handle("agents")
    collection = db_handle.agent_data
    doc = {"agent_id": agent_id, "data": data}
    data_id = collection.insert_one(doc).inserted_id
    return data_id


def load_agent_data(agent_id, db_handle=None):
    if db_handle is None:
        db_handle = get_db_handle("agents")
    collection = db_handle.agent_data
    result = list(collection.find({"agent_id": agent_id}))
    if len(result)>0:
        return result[0]["data"]
    else:
        return None


def save_game_result(agent_id, game_id, game_type, score, win,db_handle=None):
    if db_handle is None:
        db_handle = get_db_handle("agents")
    collection = db_handle.agents
    result = list(collection.find({"_id": agent_id}))
    if len(result)>0:
        agent = result[0]
    else:
        raise Exception("agent not found: {}".format(agent_id))

    if "results" in agent:
        num_games = agent["results"]["num_games"]
        avg_score = agent["results"]["avg_score"]
        agent["results"]["num_games"] += 1
        agent["results"]["avg_score"] = (avg_score*num_games+score)/(num_games+1)
        if win:
            agent["results"]["num_wins"] +=1
    else:
        agent["results"]={}
        agent["results"]["num_games"] = 1
        agent["results"]["avg_score"] = score
        agent["results"]["num_wins"] = 1 if win else 0

    collection.save(agent)


def load_game_results(game_type,db_handle=None):
    if db_handle is None:
        db_handle = get_db_handle("agents")
    collection = db_handle.agents
    result = list(collection.find({"game_type": game_type}))

    stats = []

    for agent in result:
        if "results" in agent:
            stats.append((agent, agent["results"]["num_wins"]/agent["results"]["num_games"]))

    return stats
