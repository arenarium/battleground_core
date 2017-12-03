import json
import importlib
import inspect
# import os
from .dynamic_agent import DynamicAgent
from .game_runner import GameRunner
import time


def parse_config(config):
    if isinstance(config, dict):
        return config
    try:
        with open(config, "r") as file:
            data = json.load(file)
    except OSError:
        data = json.loads(config)
    return data


def get_players(players_config):
    # TODO: retrieve player ID to use as key to dictionary
    agents = []
    for player in players_config:
        agents.append(DynamicAgent(**player))
    return dict(enumerate(agents))


def game_engine_factory(num_players, game_config):
    local_path = game_config["local_path"]
    engine_module = importlib.import_module(local_path)
    for name, obj in inspect.getmembers(engine_module):
        if name == game_config["class_name"] and inspect.isclass(obj):
            engine_class = obj
            break
    if "mods" in game_config:
        try:
            builder_path = game_config["mods"]["builder_path"]
            builder_module = importlib.import_module(builder_path)
            engine_class = builder_module.modded_class_factory(engine_class,
                                                               game_config["mods"]["mod_paths"])
        except NameError:
            pass
    engine_instance = engine_class(num_players=num_players,
                                   type=game_config["type"],
                                   **game_config["settings"])
    #
    # Idea: instead of modding the class, it might be a better idea to mod the instance:
    #
    # engine_instance = modded_instance_factory(engine_instance, game_config["mods"])
    return engine_instance


def start_session(config, save=True, game_delay=None):
    config_data = parse_config(config)
    players = get_players(config_data["players"])
    all_scores = []
    for _ in range(config_data["num_games"]):
        engine = game_engine_factory(len(players), config_data["game"])
        game_runner = GameRunner(engine, players=players, save=save)
        scores = game_runner.run_game()
        if game_delay is None:
            time.sleep(config_data["game_delay"])
        else:
            time.sleep(game_delay)
        print(scores)
        all_scores.append(scores)
    return all_scores
