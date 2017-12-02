from battleground.dynamic_agent import DynamicAgent
from games.basic_game.basic_agent import BasicAgent
from battleground.persistence import agent_data
from battleground.agent import Agent


def test_dynamic_agent_local_path():
    config = {
        "owner": "test_owner",
        "name": "test_agent",
        "local_path": "games.basic_game.basic_agent",
        "remote_path": None
    }

    da = DynamicAgent(**config)

    assert isinstance(da.agent_instance, BasicAgent)
    assert isinstance(da.move(None), dict)


def test_dynamic_agent_database():
    config = {
        "owner": "test_owner",
        "name": "test_agent",
        "game_type": "test_game",
        "local_path": "games.basic_game.basic_agent",
        "remote_path": None
    }

    agent_id = agent_data.get_agent_id(owner=config["owner"],
                                       name=config["name"],
                                       game_type=["game_type"])
    module_path = config["local_path"].replace(".", "/") + ".py"
    with open(module_path, 'r') as f:
        code_string = f.read()

    agent_data.save_agent_data(agent_id, code_string, "code")

    da = DynamicAgent(owner=config["owner"],
                      name=config["name"],
                      game_type=["game_type"],
                      from_db=True)

    assert isinstance(da.agent_instance, Agent)
    assert isinstance(da.move(None), dict)
