import pytest
import start


def test_get_dynamic_players():
    game_type = "basic_game"
    players = start.get_dynamic_players(game_type=game_type,n=5)

    assert len(players)==5
    assert isinstance(players[0],dict)
    for player in players:
        assert game_type in player["game_type"]

def test_get_game_gonfig():

    game_config = start.generate_dynamic_config(0)

    assert isinstance(game_config,dict)

    assert "game" in game_config
    assert "players" in game_config

    assert isinstance(game_config["game"],dict)
    assert isinstance(game_config["players"],list)
    assert len(game_config["players"])>0
