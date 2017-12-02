import json
import importlib
import inspect
from .dynamic_agent import DynamicAgent
from .game_runner import GameRunner
import time
from .persistence import agent_data


def parse_config(config):
    if isinstance(config, dict):
        return config
    try:
        with open(config, "r") as f:
            data = json.load(f)
    except Exception as e:
        data = json.loads(config)
    return data


def get_players(players_config, game_type):
    agents = {}
    for player in players_config:
        agent_id = agent_data.get_agent_id(player["owner"],
                                           player["name"],
                                           game_type)
        agents[str(agent_id)] = DynamicAgent(**player)
    return agents


def game_engine_factory(num_players, game_config):
    local_path = game_config["local_path"]
    engine_module = importlib.import_module(local_path)
    for name, obj in inspect.getmembers(engine_module):
        if name == game_config["class_name"] and inspect.isclass(obj):
            engine_class = obj
            break
    engine_instance = engine_class(num_players=num_players,
                                   type=game_config["type"],
                                   **game_config["settings"])
    return engine_instance


def start_session(config, save=True, game_delay=None):
    config_data = parse_config(config)
    print(config_data["game"]["type"])
    players = get_players(config_data["players"], config_data["game"]["type"])
    all_scores = []
    for i in range(config_data["num_games"]):
        engine = game_engine_factory(len(players), config_data["game"])
        gr = GameRunner(engine, players=players, save=save)
        scores = gr.run_game()

        if game_delay is None:
            time.sleep(config_data["game_delay"])
        else:
            time.sleep(game_delay)
        print(scores)
        all_scores.append(scores)

    for id, player in players.items():
        agent_data.save_agent_data(agent_id=id,
                                   data=player.get_data_to_save(),
                                   key="memory")
    return all_scores
