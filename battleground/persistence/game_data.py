from uuid import uuid4
from couchdb.client import Server
import json
from os import environ


def get_server():
    if "COUCHDB_HOST" in environ:
        host = environ["COUCHDB_HOST"]
        s = Server(host)
    else:
        s=Server()
    return s


def get_db(name=None,server=None):
    if name is None:
        name="game_states"
    if server is None:
        server=get_server()
    if name in server:
        db = server[name]
    else:
        db = server.create(name)
    return db


def get_new_id():
    doc_id = uuid4().hex
    return doc_id


def save_game_state(game_id, sequence,game_type, player_ids, game_state,db=None):
    if db is None:
        db = get_db()
    state_id = get_new_id()
    doc = {"sequence":sequence,
           "player_ids":json.dumps(player_ids),
           "game_state":json.dumps(game_state),
           "game_id":game_id,
           "game_type":game_type,
           "_id":state_id}

    db.save(doc)
    return state_id


def save_game_history(game_type, player_ids, game_states,db=None):
    game_id = get_new_id()
    if db is None:
        db = get_db()

    for i,state in enumerate(game_states):
        save_game_state(game_id=game_id,
                        sequence=i,
                        game_type=game_type,
                        player_ids=player_ids,
                        game_state=state,
                        db=db)
    return game_id


def load_game_history(game_id,db=None):
    map_fun = '''function(doc) {emit([doc.game_id], doc)}'''
    if db is None:
        db = get_db()
    result = db.query(map_fun)
    data =  {r.id:r.value for r in result[[game_id]]}
    states_in_sequence = [None]*len(data)
    for key,value in data.items():
        doc = data[key].copy()
        game_state=data[key]["game_state"]
        doc["game_state"] = json.loads(game_state)
        states_in_sequence[doc["sequence"]] = doc
    return states_in_sequence


def get_games_list(db=None):
    if db is None:
        db = get_db()
    map_fun = '''function(doc) {emit([doc.game_id,doc.game_type])}'''
    result = db.query(map_fun,'_count', group=True)
    data =  [(r.key,r.value) for r in result[:]]
    return data
