from uuid import uuid4
from pymongo import MongoClient
import json
from os import environ

global_client = None


def get_client():
    global global_client
    if global_client is None:
        if "MONGO_HOST" in environ:
            host = environ["MONGO_HOST"]
            global_client = MongoClient(host)
        else:
            global_client = MongoClient()
    return global_client


def get_db(name=None, client=None):
    if name is None:
        name = "game_states"
    if client is None:
        client = get_client()
    db = client[name]
    return db


def get_collection(name=None):
    if name is None:
        name = "game_states"
    return get_db()[name]


def get_new_id():
    doc_id = uuid4().hex
    return doc_id


def save_game_states(game_id,
                     game_type,
                     game_states,
                     collection=None):
    """
    save one or more documents to the data-store.
    game_states: [dict,...]
        each key, value will be stord as key: json(value) in the document.
        expected keys are "game_state", "last_move" and "player_ids"
    """
    if collection is None:
        collection = get_collection()
    all_docs = []
    for i, game_state in enumerate(game_states):
        doc = {
            "sequence": i,
            "game_id": game_id,
            "game_type": game_type
        }
        for key, value in game_state.items():
            assert key not in doc
            doc[key] = json.dumps(value)
        all_docs.append(doc)

    result = collection.insert_many(all_docs)
    return result


def save_game_history(game_type, game_states, collection=None):
    """
    save a sequence of documents to the data-store.
    game_states: array of dict
        each array element will be stored as one document in the doc-store.
        each key, value in each dict will be stord as key: json(value) in the document.
        expected keys are "game_state", "last_move" and "player_ids"
    """

    game_id = get_new_id()
    if collection is None:
        collection = get_collection()

    result = save_game_states(game_id=game_id,
                     game_type=game_type,
                     game_states=game_states,
                     collection=collection)
    return game_id


def load_game_history(game_id, collection=None):
    """load all states with the same game ID and return an ordered sequence"""

    if collection is None:
        collection = get_collection()
    result = collection.find({"game_id":game_id})
    data = result[:]
    states_in_sequence = [None] * result.count()
    """now decode some of the values that are json strings"""
    for loaded_doc in data:
        output_doc = {}
        for data_key in loaded_doc:
            if data_key in ["game_state", "last_move"]:  # decode these two keys, because they are special
                output_doc[data_key] = json.loads(loaded_doc[data_key])
            else:
                output_doc[data_key] = loaded_doc[data_key]
        states_in_sequence[output_doc["sequence"]] = output_doc
    return states_in_sequence


def get_games_list(game_type=None, collection=None):
    """
    get a list of unique game IDs
    """

    if collection is None:
        collection = get_collection()

    if game_type is None:
        result = collection.distinct(key="game_id")
    else:
        result = collection.distinct(key="game_id", filter={"game_type":game_type})

    return result
