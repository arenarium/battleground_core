from uuid import uuid4
from couchdb.client import Server
import json
from os import environ


def get_server():
    if "COUCHDB_HOST" in environ:
        host = environ["COUCHDB_HOST"]
        server = Server(host)
    else:
        server = Server()
    return server


def get_db(name=None, server=None):
    if name is None:
        name = "game_states"
    if server is None:
        server = get_server()
    if name in server:
        db = server[name]
    else:
        db = server.create(name)
    return db


def get_new_id():
    doc_id = uuid4().hex
    return doc_id


def save_game_state(game_id,
                    sequence,
                    game_type,
                    game_state,
                    db=None):
    """
    save one document to the data-store.
    game_state: dict
        each key, value will be stord as key: json(value) in the document.
        expected keys are "game_state", "last_move" and "player_ids"
    """
    if db is None:
        db = get_db()
    state_id = get_new_id()
    doc = {"sequence": sequence,
           "game_id": game_id,
           "game_type": game_type,
           "_id": state_id}
    for key, value in game_state.items():
        assert key not in doc
        doc[key] = json.dumps(value)

    db.save(doc)
    return state_id


def save_game_history(game_type, game_states, db=None):
    """
    save a sequence of documents to the data-store.
    game_states: array of dict
        each array element will be stored as one document in the doc-store.
        each key, value in each dict will be stord as key: json(value) in the document.
        expected keys are "game_state", "last_move" and "player_ids"
    """

    game_id = get_new_id()
    if db is None:
        db = get_db()

    for i, state in enumerate(game_states):
        save_game_state(game_id=game_id,
                        sequence=i,
                        game_type=game_type,
                        game_state=state,
                        db=db)
    return game_id


def load_game_history(game_id, db=None):
    """load all states with the same game ID and return an ordered sequence"""

    map_fun = '''function(doc) {emit([doc.game_id], doc)}'''
    if db is None:
        db = get_db()
    result = db.query(map_fun)
    data = {r.id: r.value for r in result[[game_id]]}
    states_in_sequence = [None] * len(data)
    # now decode some of the values that are json strings
    for loaded_doc in data.values():
        output_doc = loaded_doc.copy()
        for data_key in ["game_state", "last_move"]:  # decode these two keys, because they are special
            output_doc[data_key] = json.loads(loaded_doc[data_key])
        states_in_sequence[loaded_doc["sequence"]] = output_doc
    return states_in_sequence


def get_games_list(game_type=None, db=None):
    """
    get a list of unique game IDs
    """

    if db is None:
        db = get_db()
    map_fun = '''function(doc) {emit([doc.game_type,doc.game_id])}'''
    result = db.query(map_fun, '_count', group=True)

    if game_type is None:
        data = [(r.key, r.value) for r in result[:]]
    else:
        data = [(r.key, r.value) for r in result[[game_type]:[game_type, "ZZZ"]]]
    return data
