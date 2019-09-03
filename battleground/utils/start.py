import argparse
import os.path
from battleground import site_runner
from battleground.config_generator import generate_dynamic_config
from battleground.utils import init_db, populate_db_core_agents
import sys
from battleground.persistence import game_data
from datetime import datetime, timedelta

DEFAULT_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "../config/")
DEFAULT_REGISTERED_GAME_PATH = os.path.join(DEFAULT_CONFIG_PATH, "registered_games.json")


def make_path_absolute(path):
    if not os.path.isabs(path):
        if not os.path.exists(path):
            path = os.path.join(DEFAULT_CONFIG_PATH, path)
    return path


def print_scores(win_rates):
    print("Win rates:")
    for name, win_rate in win_rates.items():
        print('{}: {:1.4f}'.format(name, win_rate))


def go():
    """
    start the battleground server
    """

    sys.path.append(".")

    default_player_file_path = os.path.join(DEFAULT_CONFIG_PATH, "registered_players.json")
    default_config_file = os.path.join(DEFAULT_CONFIG_PATH, "basic_config.json")

    parser = argparse.ArgumentParser(description='Start Arenarium')
    parser.add_argument('--config', type=str, default=default_config_file)
    parser.add_argument('--registered_games', type=str, default=DEFAULT_REGISTERED_GAME_PATH)
    parser.add_argument('--dynamic', action='store_true')
    parser.add_argument('-d', action='store_true')
    parser.add_argument('--use_db', action='store_true')
    parser.add_argument('--init', action='store_true')
    parser.add_argument('--purge', action='store_true')
    parser.add_argument('--count', type=int, default=1)
    parser.add_argument('--no_save', action='store_true')
    args = parser.parse_args()

    if args.purge:
        game_data.purge_game_data(date=datetime.utcnow() - timedelta(days=14))

    if args.init:
        print('Creating indices...')
        init_db.create_indices()

        print('Creating players...')
        populate_db_core_agents.add_default_players()

        print('Done.')
    else:
        print("starting battleground ...")
        i = 0
        while i < args.count or args.d:
            i += 1
            if args.dynamic:
                print("running new dynamic config ...")
                delay = 10 if args.d else 0
                players = None if args.use_db else default_player_file_path

                # relative paths can be local or in de default config folder
                reg_games_path = make_path_absolute(args.registered_games)

                config = generate_dynamic_config(reg_games_path,
                                                 players=players,
                                                 game_delay=delay)
                win_rates = site_runner.start_session(config, save=not args.no_save)
            else:
                config_file_name = args.config

                # relative paths can be local or in de default config folder
                config_file_name = make_path_absolute(args.config)

                win_rates = site_runner.start_session(config_file_name, save=not args.no_save)
            print_scores(win_rates)


if __name__ == "__main__":
    go()
