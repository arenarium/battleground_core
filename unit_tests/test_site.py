import battleground.site_runner as site_runner
from battleground.dynamic_agent import DynamicAgent
from games.basic_game.basic_game_engine import BasicGameEngine
import json

CONFIG_DATA_FILE = "config/basic_config.json"


def test_json():
    with open(CONFIG_DATA_FILE, "r") as f:
        data = json.load(f)
    assert isinstance(data, dict)


def test_config_loader():
    data = site_runner.parse_config(CONFIG_DATA_FILE)
    assert isinstance(data, dict)
    assert "game" in data
    assert "players" in data

    with open(CONFIG_DATA_FILE, 'r') as f:
        config_string = f.read()

    data = site_runner.parse_config(config_string)
    assert isinstance(data, dict)

    assert "game" in data
    assert "players" in data


def test_get_players():
    data = site_runner.parse_config(CONFIG_DATA_FILE)
    players = site_runner.get_players(data["players"], data["game"]["type"])

    assert isinstance(players, dict)
    assert len(players) == len(data["players"])

    for key, player in players.items():
        assert isinstance(player, DynamicAgent)


def test_get_engine():
    game_config = {
        "name": "bg",
        "type": "basic_game",
        "local_path": "games.basic_game.basic_game_engine",
        "class_name": "BasicGameEngine",
        "settings": {}
    }
    engine = site_runner.game_engine_factory(2, game_config)
    assert isinstance(engine, BasicGameEngine)
    assert engine.get_game_name() == game_config["type"]


def test_run_session():
    scores = site_runner.start_session(
        CONFIG_DATA_FILE, save=False, game_delay=0)
    assert len(scores) > 0
    assert len(scores[0]) > 0

    for s in scores:
        for v in s:
            assert v >= 0


if __name__ == "__main__":
    test_json()
