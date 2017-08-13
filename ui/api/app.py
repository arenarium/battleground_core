"""
rest interface
"""

from flask import Flask, request, jsonify
from os import path, environ
import json

from battleground.persistence import game_data

app = Flask(__name__)


def do_move(game_id, data):
    raise NotImplementedError()

def get_players():
    raise NotImplementedError()

@app.route("/api/games/<game_id>")
def get_game_states(game_id):
    data = game_data.load_game_history(game_id)
    return jsonify(data)

@app.route("/api/games/")
def get_games():
    data = game_data.get_games_list()
    return jsonify(data)

@app.route("/")
def main():
    return "flask root"
