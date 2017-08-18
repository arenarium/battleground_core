import json
import os
import importlib
import inspect
from .dynamic_agent import DynamicAgent
from .game_runner import GameRunner
import time


def parse_config(config):
    if isinstance(config,dict):
        return config
    try:
        with open(config,"r") as f:
            data = json.load(f)
    except:
        data = json.loads(config)
    return data


def get_players(players_config):
    ## TODO: retreive player ID to use as key to dictionary
    agents = []
    for player in players_config:
        agents.append(DynamicAgent(**player))
    return dict(enumerate(agents))


def get_game_engine(num_players,game_config):
    local_path = game_config["local_path"]
    engine_module = importlib.import_module(local_path)
    for name, obj in inspect.getmembers(engine_module):
        if name==game_config["class_name"] and inspect.isclass(obj):
            engine_class = obj
            break
    engine_instance = engine_class(num_players =num_players,
                                   name = game_config["name"],
                                   **game_config["settings"])
    return engine_instance


def start_session(config,save=True,game_delay=None):
    config_data = parse_config(config)
    players = get_players(config_data["players"])
    all_scores = []
    for i in range(config_data["num_games"]):
        engine = get_game_engine(len(players),config_data["game"])
        gr = GameRunner(engine,players=players,save=save)
        scores = gr.run_game()
        if game_delay is None:
            time.sleep(config_data["game_delay"])
        else:
            time.sleep(game_delay)
        print(scores)
        all_scores.append(scores)
    return all_scores
