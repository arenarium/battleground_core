import pytest
from battleground.persistence import agent_data, game_data
from datetime import datetime

owner, name, game_type = "test_owner", "test_name", "test_game_type"


@pytest.fixture(scope="module")
def db_handle():
    """temporary database for testing"""
    client = game_data.get_client()
    db_handle = game_data.get_db_handle("test_db_handle")
    yield db_handle
    client.drop_database("test_db_handle")


def test_get_agent_id(db_handle):
    new_agent_id = agent_data.get_agent_id(owner, name, game_type, db_handle)
    same_agent_id = agent_data.get_agent_id(owner, name, game_type, db_handle)

    assert same_agent_id is not None
    assert new_agent_id == same_agent_id

    owners = agent_data.get_owners(db_handle)
    assert len(owners) > 0


def test_no_duplicate_ids(db_handle):
    agent_ids = []
    for _ in range(10):
        agent_id = agent_data.get_agent_id(owner, name, game_type, db_handle)
        agent_ids.append(agent_id)
    assert len(agent_ids) == 10
    assert len(set(agent_ids)) == 1

    collection = db_handle.agents
    result = list(collection.find({"owner": owner,
                                   "name": name,
                                   "game_type": game_type}))
    assert len(result) == 1


def test_get_agents(db_handle):
    global owner, name, game_type

    # add agent if not exists
    agent_data.get_agent_id(owner, name, game_type, db_handle)

    agents = agent_data.get_agents(owner, db_handle=db_handle)
    assert len(agents) > 0


def test_save_data(db_handle):

    data = {"key1": "value1", "key2": "value2"}
    agent_id = agent_data.get_agent_id(owner, name, game_type, db_handle)
    assert len(str(agent_id)) == 24

    agent_data.save_agent_data(agent_id, data, "data", db_handle=db_handle)

    loaded_data = agent_data.load_agent_data(agent_id,
                                             "data",
                                             db_handle=db_handle)
    assert loaded_data == data

    loaded_data = agent_data.load_agent_data(agent_id,
                                             "blah",
                                             db_handle=db_handle)
    assert loaded_data is None


def test_save_game_result(db_handle):
    """
    just test that function runs without errors
    """
    agent_id = agent_data.get_agent_id(owner, name, game_type, db_handle=db_handle)
    game_id = "123456"
    score = 123
    win = True
    agent_data.save_game_result(agent_id,
                                game_id,
                                game_type,
                                score,
                                win,
                                datetime.utcnow(),
                                db_handle=db_handle)

    game_stats = agent_data.load_game_results(game_type, db_handle=db_handle)

    assert len(game_stats) > 0
    assert len(game_stats[0]) == 4
    agent_ids = [x[0] for x in game_stats]
    assert str(agent_id) in agent_ids


def test_get_player_results(db_handle):
    agent_id = agent_data.get_agent_id(owner, name, game_type, db_handle=db_handle)
    agent_results = agent_data.load_agent_results(agent_id, db_handle=db_handle)

    assert len(agent_results) > 0
    cols = ['agent_id', 'game_id', 'game_type', 'score', 'win', 'time']
    for col in cols:
        assert col in agent_results[0]


def test_save_code(db_handle):
    path = "battleground/games/basic_game/basic_persistent_agent.py"
    with open(path, 'r') as file:
        code = file.read()

    agent_id = agent_data.save_agent_code(owner, name, game_type, code)
    assert agent_id is not None

    loaded_code = agent_data.load_agent_code(owner, name, game_type)

    assert loaded_code == code
