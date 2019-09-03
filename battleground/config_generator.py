from .persistence import agent_data
import random
import json
import os.path


def generate_players_config_from_db(game_type, num_players):
    agent_ids = agent_data.get_agents(game_type=game_type,
                                      has_file=True,
                                      fields=['owner', 'name'])
    # print(agent_ids)
    players = random.sample(agent_ids,
                            num_players)
    config = []
    for player in players:
        player_config = {}
        for key in ['owner', 'name']:
            player_config[key] = player[key]
        player['game_type'] = game_type
        player['from_db'] = True
        config.append(player)
    return players


def generate_players_config_from_file(file_path, game_type=None, number_of_players=None):
    """
    this is a light-weight local version to pick players for a game.
    in deployment this should be replaced with a database query.
    """
    with open(file_path, 'r') as conf:
        registered_players = json.load(conf)

    if game_type is not None:
        qualifying_players = []
        for _, player in registered_players.items():
            if game_type in player["game_type"]:
                qualifying_players.append(player)
    else:
        qualifying_players = registered_players

    if not qualifying_players:
        raise IndexError("No qualifying players found.")

    if number_of_players is not None:
        players = []
        for _ in range(number_of_players):
            players.append(random.choice(qualifying_players))
    else:
        players = qualifying_players
    return players


def generate_dynamic_config(registered_games_spec,
                            game_delay=None,
                            players=None,
                            game_type=None,
                            num_players=3,
                            move_delay=0,
                            max_turns=1000,
                            num_games=3):

    # check if path to file or list of dicts
    try:
        if os.path.exists(registered_games_spec):
            with open(registered_games_spec, 'r') as conf:
                registered_games = json.load(conf)
    except Exception as e:
        try:
            assert 'type' in registered_games_spec[0]
            registered_games = registered_games_spec
        except Exception as e:
            raise Exception('Could not interpred games spec: '+str(e))

    if game_type is None:
        game_spec = random.choice(registered_games)
    else:
        registered_games = {x["type"]: x for x in registered_games}
        assert game_type in registered_games
        game_spec = registered_games[game_type]

    if players is None:
        players = generate_players_config_from_db(game_spec["type"], num_players)
    elif isinstance(players, list):
        players = players
    else:
        players = generate_players_config_from_file(game_type=game_spec["type"],
                                                    number_of_players=num_players,
                                                    file_path=players)

    config = {
        "game": game_spec,
        "players": players,
        "num_games": num_games,
        "max_turns": max_turns,
        "move_delay": move_delay,
        "game_delay": game_delay,
    }

    return config
