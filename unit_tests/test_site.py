import pytest
import battleground.site_runner as site_runner
from  battleground.dynamic_agent import DynamicAgent
from battleground.game_engine import GameEngine
from games.basic_game.basic_game_engine import BasicGameEngine
import json
config_data_file = "config/basic_config.json"

def test_json():
    with open(config_data_file,"r") as f:
        data = json.load(f)
    assert isinstance(data,dict)



def test_config_loader():
    data = site_runner.parse_config(config_data_file)
    assert isinstance(data,dict)
    assert "game" in data
    assert "players" in data

    with open(config_data_file,'r') as f:
        config_string = f.read()

    data = site_runner.parse_config(config_string)
    assert isinstance(data,dict)

    assert "game" in data
    assert "players" in data


def test_get_players():
    data = site_runner.parse_config(config_data_file)
    players = site_runner.get_players(data["players"])

    assert isinstance(players,dict)
    assert len(players) == len(data["players"])

    for key,player in players.items():
        assert isinstance(player,DynamicAgent)


def test_get_engine():
    game_config={
        "name":"bg",
        "type":"basic_game",
        "local_path":"games.basic_game.basic_game_engine",
        "class_name":"BasicGameEngine",
        "settings":{}
      }
    engine = site_runner.game_engine_factory(2,game_config)
    assert isinstance(engine,BasicGameEngine)
    assert engine.get_game_name() == game_config["type"]

def test_run_session():
    scores = site_runner.start_session(config_data_file,save=False,game_delay=0)
    assert len(scores)>0
    assert len(scores[0])>0

    for s in scores:
        for v in s:
            assert v>=0


if __name__ == "__main__":
    test_json()
