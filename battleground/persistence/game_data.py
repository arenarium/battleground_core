#from uuid import uuid4
import pymongo
from pymongo import MongoClient
import bson
import json
from os import environ

import datetime

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


def get_db_handle(name=None, client=None):
    if name is None:
        name = "game_states"
    if client is None:
        client = get_client()
    db_handle = client[name]
    return db_handle


def save_game_states(game_id,
                     game_type,
                     game_states,
                     db_handle=None):
    """
    save one or more documents to the data-store.
    game_states: [dict,...]
        each key, value will be stord as key: json(value) in the document.
        expected keys are "game_state", "last_move" and "player_ids"
    """
    if db_handle is None:
        db_handle = get_db_handle()
    collection = db_handle.game_states

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


def save_game_meta_data(game_type, num_states,utc_time=None,db_handle=None):
    if db_handle is None:
        db_handle = get_db_handle()
    if utc_time is None:
        utc_time = str(datetime.datetime.utcnow())
    doc = {"game_type":game_type,"utc_time":utc_time,"num_states":num_states}
    game_id = db_handle.games.insert_one(doc).inserted_id
    return game_id


def save_game_history(game_type, game_states, db_handle=None):
    """
    save a sequence of documents to the data-store.
    game_states: array of dict
        each array element will be stored as one document in the doc-store.
        each key, value in each dict will be stord as key: json(value) in the document.
        expected keys are "game_state", "last_move" and "player_ids"
    """

    if db_handle is None:
        db_handle = get_db_handle()

    game_id = save_game_meta_data(game_type=game_type,
                                  num_states = len(game_states),
                                  db_handle=db_handle)

    save_game_states(game_id=game_id,
                     game_type=game_type,
                     game_states=game_states,
                     db_handle=db_handle)
    return game_id


def load_game_history(game_id, db_handle=None):
    """load all states with the same game ID and return an ordered sequence"""

    if db_handle is None:
        db_handle = get_db_handle()

    if not isinstance(game_id,bson.ObjectId):
        game_id = bson.ObjectId(str(game_id))

    collection = db_handle.game_states

    result = collection.find({"game_id":game_id})
    data = result[:]
    states_in_sequence = [None] * result.count()

    # now decode some of the values that are json strings
    for loaded_doc in data:
        output_doc = {}
        for data_key in loaded_doc:
            if data_key in ["game_state", "last_move"]:
                # decode these two keys, because they are special
                output_doc[data_key] = json.loads(loaded_doc[data_key])
            else:
                output_doc[data_key] = loaded_doc[data_key]
        states_in_sequence[output_doc["sequence"]] = output_doc
    return states_in_sequence


def get_games_list(game_type=None, db_handle=None):
    """
    get a list of unique game IDs
    """

    if db_handle is None:
        db_handle = get_db_handle()

    collection = db_handle.games

    if game_type is None:
        result = collection.find(sort=[('utc_time', pymongo.DESCENDING)])
    else:
        result = collection.find(sort=[('utc_time', pymongo.DESCENDING)],
                                 filter={"game_type":game_type})

    return result
