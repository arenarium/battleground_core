import pytest
import json
from ui.api import app


def test_games_list():
    test_app = app.app.test_client()

    reponse = test_app.get("/api/games/")
    assert reponse.status_code == 200
    games_list_string = reponse.data.decode()

    games_list = json.loads(games_list_string)

    assert len(games_list)>=0
    return games_list

def test_game_moves():
    games_list = test_games_list()
    test_app = app.app.test_client()


    game_id = games_list[0][0][0]
    num_states = games_list[0][1]

    reponse = test_app.get("/api/games/"+str(game_id))
    assert reponse.status_code == 200
    states_string = reponse.data.decode()
    states = json.loads(states_string)
    assert len(states)==num_states
    assert isinstance(states[0],dict)
    assert len(states[0])>=1
