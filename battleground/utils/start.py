import argparse
import os.path
from battleground import site_runner
from battleground.config_generator import generate_dynamic_config

DEFAULT_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "../config/")
DEFAULT_REGISTERED_GAME_PATH = os.path.join(DEFAULT_CONFIG_PATH, "registered_games.json")


def go():
    # time.sleep(1)
    default_player_file_path = os.path.join(DEFAULT_CONFIG_PATH, "registered_players.json")
    default_config_file = os.path.join(DEFAULT_CONFIG_PATH, "basic_config.json")

    parser = argparse.ArgumentParser(description='Start Arenarium')
    parser.add_argument('--config', type=str, default=default_config_file)
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
            config = generate_dynamic_config(DEFAULT_REGISTERED_GAME_PATH,
                                             players=players,
                                             delay=delay)
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
