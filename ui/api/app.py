"""
rest interface
"""

from flask import Flask, request, jsonify
from os import path, environ
import json

from battleground.persistence import game_data
from battleground.persistence import agent_data

app = Flask(__name__)


def do_move(game_id, data):
    raise NotImplementedError()


def get_players():
    raise NotImplementedError()


@app.route("/api/states/<game_id>")
def get_game_states(game_id):
    data = game_data.load_game_history(game_id)
    output = []
    for doc in data:
        doc["_id"] = str(doc["_id"])
        doc["game_id"] = str(doc["game_id"])
        output.append(doc)
    return jsonify(output)


@app.route("/api/games/<game_type>")
def get_games(game_type):
    data = game_data.get_games_list(game_type=game_type)[0:10]
    output = []
    for doc in data:
        doc["_id"] = str(doc["_id"])
        output.append(doc)
    return jsonify(output)


@app.route("/api/games/")
def get_games_types():
    data = game_data.get_games_list()[0:10]
    output = []
    for doc in data:
        doc["_id"] = str(doc["_id"])
        output.append(doc)
    return jsonify(output)


@app.route("/api/stats/")
def get_game_results():
    data = agent_data.load_game_results(game_type="basic_game")
    return jsonify(data)


@app.route("/api/")
def main():
    return "flask root"
