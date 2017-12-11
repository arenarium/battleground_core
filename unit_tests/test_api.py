import pytest
import json
import sys

sys.path.append("ui/api")
import app


def test_games_list():
    test_app = app.app.test_client()

    reponse = test_app.get("/api/games/")
    assert reponse.status_code == 200

    games_list_string = reponse.data.decode()
    games_list = json.loads(games_list_string)
    # at least some games should be in the DB
    assert len(games_list) > 0
    return games_list


def test_games_list_selector():
    test_app = app.app.test_client()

    # this game type should not exist
    response = test_app.get("/api/games/basd02938isafd")
    assert response.status_code == 200

    games_list_string = response.data.decode()
    games_list = json.loads(games_list_string)
    assert len(games_list) == 0

    # this game type should exist
    response = test_app.get("/api/games/basic_game")
    assert response.status_code == 200

    games_list_string = response.data.decode()
    games_list = json.loads(games_list_string)
    assert len(games_list) > 0


def test_game_moves():
    games_list = test_games_list()
    test_app = app.app.test_client()

    game_id = games_list[0]["_id"]
    num_states = games_list[0]["num_states"]

    response = test_app.get("/api/states/" + str(game_id))
    assert response.status_code == 200

    states_string = response.data.decode()
    states = json.loads(states_string)
    assert len(states) == num_states
    assert isinstance(states[0], dict)
    assert len(states[0]) >= 1
