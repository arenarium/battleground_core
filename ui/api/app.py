"""
rest interface
"""

from flask import Flask, request, jsonify
from os import path, environ
import json

import game_data

app = Flask(__name__)


def do_move(game_id, data):
    raise NotImplementedError()


def get_players():
    raise NotImplementedError()


@app.route("/api/states/<game_id>")
def get_game_states(game_id):
    data = game_data.load_game_history(game_id)
    return jsonify(data)


@app.route("/api/games/<game_type>")
def get_games(game_type):
    data = game_data.get_games_list(game_type=game_type)
    return jsonify(data)


@app.route("/api/games/")
def get_games_types():
    data = game_data.get_games_list()
    return jsonify(data)


@app.route("/api/")
def main():
    return "flask root"
