import argparse
import json
import random
import time
from battleground import site_runner


def get_dynamic_players(game_type,n):
    """
    this is a light-weight local version to pick players for a game.
    in deployment this should be replaced with a database query.
    """
    with open("config/registered_players.json",'r') as f:
        registered_players = json.load(f)
    qualifying_players = []
    for name,p in registered_players.items():
        if game_type in p["game_type"]:
            qualifying_players.append(p)

    players=[]
    for i in range(n):
        players.append(random.choice(qualifying_players))
    return players


def generate_dynamic_config(game_delay):
    with open("config/registered_games.json",'r') as f:
        registered_games = json.load(f)

    game_spec = random.choice(registered_games)

    players = get_dynamic_players(game_spec["type"],3)

    config = {
    "game":game_spec,
    "players":players,
    "num_games":3,
    "max_turns":1000,
    "move_delay":0.1,
    "game_delay":game_delay,
    }

    return config


def go():
    time.sleep(3)
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--config',type=str,default="config/basic_config.json")
    parser.add_argument('--dynamic', action='store_true')
    parser.add_argument('-d', action='store_true')
    parser.add_argument('--count', type=int, default=1)
    args = parser.parse_args()
    print("starting battleground ...")
    i=0
    while i < args.count or args.d:
        i+=1
        if args.dynamic:
            print("running new dynamic config ...")
            delay = 60 if args.d else 0
            config = generate_dynamic_config(delay)
            #print(config)
            site_runner.start_session(config)
        else:
            site_runner.start_session(args.config)


if __name__ == "__main__":
    go()
