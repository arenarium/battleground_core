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
        with open(config, "r") as file:
            data = json.load(file)
    except OSError:
        data = json.loads(config)
    return data


def get_players(players_config, game_type):
    agents = {}
    for player in players_config:
        agent_id = agent_data.get_agent_id(owner=player["owner"],
                                           name=player["name"],
                                           game_type=game_type)
        if "game_type" not in player:
            player["game_type"] = game_type
        agents[str(agent_id)] = DynamicAgent(**player)
    return agents


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


def run_session(engine, players, num_games, save=True, game_delay=None):
    all_scores = []

    for agent_id, player in players.items():
        memory = agent_data.load_agent_data(agent_id=agent_id,
                                            key="memory")
        player.set_memory(memory)

    for _ in range(num_games):
        game_runner = GameRunner(engine, players=players, save=save)
        scores = game_runner.run_game()

        if game_delay is not None:
            time.sleep(game_delay)

        print(scores)
        all_scores.append(scores)
        engine.reset()

    for player_id, player in players.items():
        agent_data.save_agent_data(agent_id=player_id,
                                   data=player.get_memory(),
                                   key="memory")
    return all_scores


def start_session(config, save=True, game_delay=None):
    config_data = parse_config(config)
    num_games = config_data["num_games"]
    print(config_data["game"]["type"])

    players = get_players(config_data["players"], config_data["game"]["type"])
    engine = game_engine_factory(num_players=len(players),
                                 game_config=config_data["game"])
    all_scores = run_session(engine,
                             players,
                             num_games,
                             save=save,
                             game_delay=game_delay)
    return all_scores
