import pytest
from battleground.persistence import game_data
from games.basic_game import basic_persistent_agent

owner, name, game_type = "test_owner", "test_name", "test_game_type"


@pytest.fixture(scope="module")
def db_handle():
    """temporary database for testing"""
    c = game_data.get_client()
    db_handle = game_data.get_db_handle("test_db_handle")
    yield db_handle
    c.drop_database("test_db_handle")


def test_memory_set():
    agent = basic_persistent_agent()


def test_with_engine():
    pass
