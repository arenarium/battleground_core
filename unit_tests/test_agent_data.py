import pytest
from battleground.persistence import agent_data, game_data


owner, name, game_type = "test_owner", "test_name", "test_game_type"


@pytest.fixture(scope="module")
def db_handle():
    """temporary database for testing"""
    c = game_data.get_client()
    db_handle = game_data.get_db_handle("test_db_handle")
    yield db_handle
    c.drop_database("test_db_handle")


def test_get_agent_id(db_handle):
    new_agent_id = agent_data.get_agent_id(owner, name, game_type, db_handle)
    same_agent_id = agent_data.get_agent_id(owner, name, game_type, db_handle)

    assert same_agent_id is not None
    assert new_agent_id == same_agent_id


def test_get_agents(db_handle):
    global owner, name, game_type

    # add agent if not exists
    agent_data.get_agent_id(owner, name, game_type, db_handle)

    agents = agent_data.get_agents(owner)
    assert len(agents) > 0


def test_save_data(db_handle):

    data = {"key1": "value1", "key2": "value2"}
    agent_id = agent_data.get_agent_id(owner, name, game_type, db_handle)
    assert len(str(agent_id)) == 24

    agent_data.save_agent_data(agent_id, data, "data", db_handle=db_handle)

    loaded_data = agent_data.load_agent_data(
        agent_id, "data", db_handle=db_handle)
    assert loaded_data == data

    loaded_data = agent_data.load_agent_data(
        agent_id, "blah", db_handle=db_handle)
    assert loaded_data is None


def test_save_game_result(db_handle):
    """
    just test that function runs without errors
    """
    agent_id = agent_data.get_agent_id(owner, name, game_type, db_handle)
    game_id = "123456"
    score = 123
    win = True
    agent_data.save_game_result(
        agent_id,
        game_id,
        game_type,
        score,
        win,
        db_handle=db_handle)


def test_get_game_stats(db_handle):
    game_stats = agent_data.load_game_results(game_type, db_handle=db_handle)

    assert len(game_stats) > 0
    assert len(game_stats[0]) == 3
