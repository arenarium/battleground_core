from .persistence import agent_data
import random
import json


def generate_players_config_from_db(game_type, num_players):
    agent_ids = agent_data.get_agents(game_type=game_type)
    players = random.sample(agent_ids, num_players, fields=['owner', 'name'])
    config = []
    for player in players:
        player_config = {}
        for key in ['owner', 'name']:
            player_config[key] = player[key]
        player['game_type'] = game_type
        player['from_db'] = True
        config.append(player)
    return players


def generate_players_config_from_file(game_type, number_of_players, file_path):
    """
    this is a light-weight local version to pick players for a game.
    in deployment this should be replaced with a database query.
    """
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


def generate_dynamic_config(file_path, game_delay=None, players=None, game_type=None):
    with open(file_path, 'r') as conf:
        registered_games = json.load(conf)

    if game_type is None:
        game_spec = random.choice(registered_games)
    else:
        registered_games = {x["name"]: x for x in registered_games}
        assert game_type in registered_games
        game_spec = registered_games[game_type]

    if players is None:
        players = generate_players_config_from_db(game_spec["type"], 3)

    config = {
        "game": game_spec,
        "players": players,
        "num_games": 3,
        "max_turns": 1000,
        "move_delay": 0.1,
        "game_delay": game_delay,
    }

    return config
