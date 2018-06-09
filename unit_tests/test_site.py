import battleground.site_runner as site_runner
from battleground.dynamic_agent import DynamicAgent
from battleground.games.basic_game.basic_game_engine import BasicGameEngine
import json
import os.path

DEFAULT_CONFIG_PATH = "battleground/config/"
CONFIG_DATA_FILE = os.path.join(DEFAULT_CONFIG_PATH, "basic_config.json")


def test_json():
    with open(CONFIG_DATA_FILE, "r") as file:
        data = json.load(file)
    assert isinstance(data, dict)


def test_config_loader():
    data = site_runner.parse_config(CONFIG_DATA_FILE)
    assert isinstance(data, dict)
    assert "game" in data
    assert "players" in data

    with open(CONFIG_DATA_FILE, 'r') as file:
        config_string = file.read()

    data = site_runner.parse_config(config_string)
    assert isinstance(data, dict)

    assert "game" in data
    assert "players" in data


def test_assign_agents():
    data = site_runner.parse_config(CONFIG_DATA_FILE)
    players = site_runner.assign_agents(data["players"], data["game"]["type"])

    assert isinstance(players, tuple)
    assert len(players) == len(data["players"])

    for _, player in players:
        assert isinstance(player, DynamicAgent)


def test_get_engine():
    game_config = {
        "name": "bg",
        "type": "basic_game",
        "local_path": "battleground.games.basic_game.basic_game_engine",
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

    for key, score in scores.items():
        assert score >= 0


if __name__ == "__main__":
    test_json()
