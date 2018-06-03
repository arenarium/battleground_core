import argparse
import os.path
from battleground import site_runner
from battleground.config_generator import generate_dynamic_config

DEFAULT_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "../config/")
DEFAULT_REGISTERED_GAME_PATH = os.path.join(DEFAULT_CONFIG_PATH, "registered_games.json")


def make_path_absolute(path):
    if not os.path.isabs(path):
        if not os.path.exists(path):
            path = os.path.join(DEFAULT_CONFIG_PATH, path)
    return path


def go():
    """
    start the battleground server
    """
    default_player_file_path = os.path.join(DEFAULT_CONFIG_PATH, "registered_players.json")
    default_config_file = os.path.join(DEFAULT_CONFIG_PATH, "basic_config.json")

    parser = argparse.ArgumentParser(description='Start Arenarium')
    parser.add_argument('--config', type=str, default=default_config_file)
    parser.add_argument('--registered_games', type=str, default=DEFAULT_REGISTERED_GAME_PATH)
    parser.add_argument('--dynamic', action='store_true')
    parser.add_argument('-d', action='store_true')
    parser.add_argument('--use_db', action='store_true')

    parser.add_argument('--count', type=int, default=1)
    args = parser.parse_args()
    print("starting battleground ...")
    i = 0
    while i < args.count or args.d:
        i += 1
        if args.dynamic:
            print("running new dynamic config ...")
            delay = 60 if args.d else 0
            players = None if args.use_db else default_player_file_path

            # relative paths can be local or in de default config folder
            reg_games_path = make_path_absolute(args.registered_games)

            config = generate_dynamic_config(reg_games_path,
                                             players=players,
                                             game_delay=delay)
            site_runner.start_session(config)
        else:
            config_file_name = args.config

            # relative paths can be local or in de default config folder
            config_file_name = make_path_absolute(args.config)

            site_runner.start_session(config_file_name)


if __name__ == "__main__":
    go()
