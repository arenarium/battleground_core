from battleground import config_generator
from battleground.persistence import agent_data
import os.path

DEFAULT_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "../battleground/config/")
DEFAULT_REGISTERED_GAME_PATH = os.path.join(DEFAULT_CONFIG_PATH, "registered_games.json")
DEFAULT_REGISTERED_AGENT_PATH = os.path.join(DEFAULT_CONFIG_PATH, "registered_players.json")


def test_get_dynamic_players():
    game_type = "basic_game"
    players = config_generator.generate_players_config_from_file(
        file_path=DEFAULT_REGISTERED_AGENT_PATH,
        game_type=game_type,
        number_of_players=5)

    assert len(players) == 5
    assert isinstance(players[0], dict)
    for player in players:
        assert game_type in player["game_type"]


def test_get_game_config():
    game_config = config_generator.generate_dynamic_config(
        file_path=DEFAULT_REGISTERED_GAME_PATH,
        players=DEFAULT_REGISTERED_AGENT_PATH
    )

    assert isinstance(game_config, dict)

    assert "game" in game_config
    assert "players" in game_config

    assert isinstance(game_config["game"], dict)
    assert isinstance(game_config["players"], list)
    assert len(game_config["players"]) > 0


def test_get_players_from_db():
    # store some agents
    with open('battleground/games/basic_game/basic_agent.py', 'r') as f:
        code = f.read()
    for i in range(2):
        agent_data.save_agent_code('test_owner',
                                   'test name {}'.format(i),
                                   'test_game',
                                   code)
    game_type = 'test_game'
    num_players = 2
    players = config_generator.generate_players_config_from_db(game_type, num_players)
    print(players)
