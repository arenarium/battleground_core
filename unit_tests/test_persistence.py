import pytest
from battleground.persistence import game_data
from couchdb.client import Server
import uuid
import random

@pytest.fixture(scope="module")
def db():
    s = game_data.get_server()
    db = game_data.get_db("test_db",s)
    yield db
    del s["test_db"]

def test_connection():
    s = game_data.get_server()
    version = s.version()
    print(version)
    assert isinstance(version,str)

def test_game_id():
    id1 = game_data.get_new_id()
    assert isinstance(id1,str)
    assert len(id1)==32
    id2 = game_data.get_new_id()
    assert isinstance(id2,str)
    assert len(id2)==32
    assert id1 != id2

def test_save_state(db):
    test_state = {"k_a":"v_a","k_b":2,"k_c":None}
    game_id = game_data.get_new_id()
    state_id = game_data.save_game_state(game_id, 0,"test_game", [0,1,2,3],test_state,db=db)
    assert isinstance(state_id,str)
    assert len(state_id)==32
    loaded_states = game_data.load_game_history(game_id,db=db)
    assert len(loaded_states)==1

    assert state_id == loaded_states[0]["_id"]

    for key,value in test_state.items():
        assert isinstance(loaded_states[0]["game_state"],dict)
        assert loaded_states[0]["game_state"][key] == value


def test_save_game_history(db):
    test_states = []
    for i in range(10):
        test_states.append({"k_a":random.randint(0,1000)})

    game_id = game_data.save_game_history("test_game",[0,1,2,3],test_states,db=db)

    loaded_states = game_data.load_game_history(game_id,db=db)

    assert len(loaded_states)==10

    #sequence_states = loaded_states#{s["sequence"]:s["game_state"] for s in loaded_states.values()}

    for i,state in enumerate(test_states):
        assert state == loaded_states[i]["game_state"]


def test_game_list(db):
    data = game_data.get_games_list(db)
    assert len(data)>0
    assert len(data[0])==2
    assert len(data[0][0])==2
    assert data[0][1]%1 == 0 # is int


if __name__ == "__main__":
    test_connection()
