from battleground.dynamic_agent import DynamicAgent
from games.basic_game.basic_agent import BasicAgent


def test_dynamic_agent():
    config = {
        "owner": "test_owner",
        "name": "test_agent",
        "local_path": "games.basic_game.basic_agent",
        "remote_path": None
    }

    dynamic_agent = DynamicAgent(**config)

    assert isinstance(dynamic_agent.agent_instance, BasicAgent)
    assert isinstance(dynamic_agent.move(None), dict)
