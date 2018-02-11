from battleground.dynamic_agent import DynamicAgent
from battleground.games.basic_game.basic_agent import BasicAgent
from battleground.persistence import agent_data
from battleground.agent import Agent


def test_dynamic_agent_local_path():
    config = {
        "owner": "test_owner",
        "name": "test_agent",
        "class_name": "BasicAgent",
        "local_path": "battleground.games.basic_game.basic_agent",
        "remote_path": None
    }

    dynamic_agent = DynamicAgent(**config)

    assert isinstance(dynamic_agent.agent_instance, BasicAgent)
    assert isinstance(dynamic_agent.move(None), dict)


def test_dynamic_agent_database():
    config = {
        "owner": "test_owner",
        "name": "test_agent",
        "game_type": "test_game",
        "class_name": "BasicAgent",
        "local_path": "battleground.games.basic_game.basic_agent",
        "remote_path": None
    }
    # create an agent ID
    agent_id = agent_data.get_agent_id(owner=config["owner"],
                                       name=config["name"],
                                       game_type=config["game_type"])

    # load file
    module_path = config["local_path"].replace(".", "/") + ".py"
    with open(module_path, 'r') as file:
        code_string = file.read()

    # save to database
    agent_data.save_agent_data(agent_id, code_string, "code")

    # test loading from database
    dynamic_agent = DynamicAgent(owner=config["owner"],
                                 name=config["name"],
                                 game_type=config["game_type"],
                                 class_name=config["class_name"],
                                 from_db=True)

    assert isinstance(dynamic_agent.agent_instance, Agent)
    assert isinstance(dynamic_agent.move(None), dict)
