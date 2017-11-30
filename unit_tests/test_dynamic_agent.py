from battleground.dynamic_agent import DynamicAgent
from games.basic_game.basic_agent import BasicAgent


def test_dynamic_agent():
    config = {
        "owner": "test_owner",
        "name": "test_agent",
        "local_path": "games.basic_game.basic_agent",
        "remote_path": None
    }

    da = DynamicAgent(**config)

    assert isinstance(da.agent_instance, BasicAgent)
    assert isinstance(da.move([0], None), dict)
