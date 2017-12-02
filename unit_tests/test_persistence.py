import pytest
from battleground.persistence import game_data
import uuid
import random


@pytest.fixture(scope="module")
def db_handle():
    """temporary database for testing"""
    c = game_data.get_client()
    db_handle = game_data.get_db_handle("test_db_handle")
    yield db_handle
    c.drop_database("test_db_handle")


def test_connection():
    c = game_data.get_client()
    connection_info = c.server_info()
    print(connection_info)
    assert isinstance(connection_info, dict)


def test_game_id(db_handle):
    """generate a unique ID"""

    id1 = game_data.save_game_meta_data(
        "test_game", num_states=0, db_handle=db_handle)
    assert len(str(id1)) == 24
    id2 = game_data.save_game_meta_data(
        "test_game2", num_states=0, db_handle=db_handle)
    assert len(str(id2)) == 24
    assert id1 != id2


def test_save_state(db_handle):
    """save a single game state"""

    test_state = {"game_state": {"k_a": "v_a", "k_b": 2, "k_c": None},
                  "last_move": {"move": "a move"}}
    game_id = game_data.save_game_meta_data(
        "test_game2", num_states=0, db_handle=db_handle)
    state_ids = game_data.save_game_states(
        game_id, "test_game", [test_state], db_handle=db_handle).inserted_ids
    assert len(state_ids) == 1

    loaded_states = game_data.load_game_history(game_id, db_handle=db_handle)
    assert len(loaded_states) == 1

    assert state_ids[0] == loaded_states[0]["_id"]
    for key, value in test_state.items():
        assert isinstance(loaded_states[0][key], dict)
        for key2, value2 in value.items():
            assert loaded_states[0][key][key2] == value2


def test_save_game_history(db_handle):
    """save a sequence of game states"""

    test_states = []
    for i in range(10):
        test_states.append({"game_state": {"k_a": random.randint(0, 1000)},
                            "last_move": {"k_move": random.randint(0, 1000)}})

    game_id = game_data.save_game_history(
        "test_game", test_states, db_handle=db_handle)

    loaded_states = game_data.load_game_history(game_id, db_handle=db_handle)

    assert len(loaded_states) == 10

    # sequence_states = loaded_states#{s["sequence"]:s["game_state"] for s in
    # loaded_states.values()}

    for i, state in enumerate(test_states):
        assert state["game_state"] == loaded_states[i]["game_state"]
        assert state["last_move"] == loaded_states[i]["last_move"]


def test_game_list(db_handle):
    """get list of games"""

    data = game_data.get_games_list(db_handle=db_handle)
    assert data.count() > 0
    assert len(str(data[0]["_id"])) == 24

    for doc in data:
        assert "game_type" in doc
        assert "utc_time" in doc


def test_game_list_selector(db_handle):
    """get list of games"""

    data = game_data.get_games_list(
        db_handle=db_handle,
        game_type="teskdsajhasde")
    assert data.count() == 0

    data = game_data.get_games_list(db_handle=db_handle, game_type="test_game")
    assert data.count() > 0
    assert len(str(data[0]["_id"])) == 24


if __name__ == "__main__":
    test_connection()
