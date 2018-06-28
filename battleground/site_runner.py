import json
import importlib
import inspect
import os
from .dynamic_agent import DynamicAgent
from .game_runner import GameRunner
import time
from .persistence import agent_data
from . import fallback_agent
from .utils.collections_ import DefaultOrderedDict


def get_win_rate(names, scores):
    rate = DefaultOrderedDict(lambda: 0)
    for score in scores:
        for name, points in zip(names, score):
            rate[name] += int((points == max(score) and points != min(score)))
    for key in rate.keys():
        rate[key] /= len(scores)
    return rate


def parse_config(config):
    if isinstance(config, dict):
        return config
    try:
        with open(config, "r") as file:
            data = json.load(file)
    except OSError:
        data = json.loads(config)
    return data


def assign_agents(players_config, game_type, save=True):
    """
    Create agent objects following the specification of players_config
    returns a list of tuples (id, agent object)
    duplicate ids are permitted, this corresponds to the same agent being instatiated twice.
    """
    agents = []  # will contain tuples of (id, object)
    for i, player in enumerate(players_config):
        if save:
            agent_id = agent_data.get_agent_id(owner=player["owner"],
                                               name=player["name"],
                                               game_type=game_type)
        else:
            agent_id = i

        if 'agent_id' not in player.keys():
            player['agent_id'] = agent_id
        # print(player)
        # append tuple to agent list
        try:
            agent_object = DynamicAgent(**player, save=save)
        except Exception as e:
            if os.environ.get('DEBUG') == 'True':
                raise e
            else:
                print(e)
                agent_object = fallback_agent.FallbackAgent()

        agents.append((str(agent_id), agent_object))
    return tuple(agents)  # return immutable version


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


def run_session(engine,
                agent_objects,
                num_games,
                save=True,
                game_delay=None,
                max_turns=None):
    all_scores = []

    if save:
        for agent_id, player in agent_objects:
            # load memory for agent (needed to enable long-term learning)
            memory = agent_data.load_agent_data(agent_id=agent_id,
                                                key="memory")
            player.set_memory(memory)

    for _ in range(num_games):
        # play multiple games
        game_runner = GameRunner(game_engine=engine,
                                 agent_objects=agent_objects,
                                 save=save,
                                 max_turns=max_turns)

        scores = game_runner.run_game()

        # use delay if set
        if game_delay is not None:
            time.sleep(game_delay)

        print(scores)
        all_scores.append(scores)
        engine.reset()

    if save:
        for agent_id, player in agent_objects:
            # persist memory for agent (needed to enable long-term learning)
            agent_data.save_agent_data(agent_id=agent_id,
                                       data=player.get_memory(),
                                       key="memory")
    return all_scores


def start_session(config, save=True, game_delay=None, run=True):
    # config can be file, dict, or json string, parse these into a dict.
    config_data = parse_config(config)
    num_games = config_data["num_games"]
    print(config_data["game"]["type"])

    if game_delay is None and 'game_delay' in config_data:
        game_delay = config_data['game_delay']

    # generate the agent instances from configuration files.
    agent_objects = assign_agents(players_config=config_data["players"],
                                  game_type=config_data["game"]["type"],
                                  save=save)

    # generate engine instance from configuration
    engine = game_engine_factory(num_players=len(agent_objects),
                                 game_config=config_data["game"])

    # setting run=False is used for testing
    if run:
        # run games and return scores
        if 'max_turns' in config_data:
            max_turns = config_data['max_turns']
        else:
            max_turns = None

        all_scores = run_session(engine,
                                 agent_objects,
                                 num_games,
                                 save=save,
                                 game_delay=game_delay,
                                 max_turns=max_turns)
        names = [agent['name'] for agent in config_data["players"]]
        return get_win_rate(names, all_scores)
    else:
        # used for testing
        return [agent_objects, engine]
