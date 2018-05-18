import argparse
import json
import random
import os.path
from battleground import site_runner

DEFAULT_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "../config/")


def get_dynamic_players(game_type, number_of_players):
    """
    this is a light-weight local version to pick players for a game.
    in deployment this should be replaced with a database query.
    """
    file_path = os.path.join(DEFAULT_CONFIG_PATH, "registered_players.json")
    with open(file_path, 'r') as conf:
        registered_players = json.load(conf)
    qualifying_players = []
    for _, player in registered_players.items():
        if game_type in player["game_type"]:
            qualifying_players.append(player)

    if not qualifying_players:
        raise IndexError("No qualifying players found.")

    players = []
    for _ in range(number_of_players):
        players.append(random.choice(qualifying_players))
    return players


def generate_dynamic_config(game_delay, game_name=None, players=None):
    file_path = os.path.join(DEFAULT_CONFIG_PATH, "registered_games.json")
    with open(file_path, 'r') as conf:
        registered_games = json.load(conf)

    if game_name is None:
        game_spec = random.choice(registered_games)
    else:
        registered_games = {x["name"]: x for x in registered_games}
        game_spec = registered_games[game_name]

    if players is None:
        players = get_dynamic_players(game_spec["type"], 3)

    config = {
        "game": game_spec,
        "players": players,
        "num_games": 3,
        "max_turns": 1000,
        "move_delay": 0.1,
        "game_delay": game_delay,
    }

    return config


def go():
    # time.sleep(1)

    default_config_file = os.path.join(DEFAULT_CONFIG_PATH, "basic_config.json")

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--config', type=str, default=default_config_file)
    parser.add_argument('--dynamic', action='store_true')
    parser.add_argument('-d', action='store_true')
    parser.add_argument('--count', type=int, default=1)
    args = parser.parse_args()
    print("starting battleground ...")
    i = 0
    while i < args.count or args.d:
        i += 1
        if args.dynamic:
            print("running new dynamic config ...")
            delay = 60 if args.d else 0
            config = generate_dynamic_config(delay)
            site_runner.start_session(config)
        else:
            config_file_name = args.config

            # relative paths can be local or in de default config folder
            if not os.path.isabs(args.config):
                if not os.path.exists(args.config):
                    config_file_name = os.path.join(DEFAULT_CONFIG_PATH, args.config)

            site_runner.start_session(config_file_name)


if __name__ == "__main__":
    go()
