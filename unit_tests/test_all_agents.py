import pytest
from battleground.dynamic_agent import DynamicAgent
from battleground.site_runner import start_session
import glob
import json
import os.path

import os


@pytest.fixture(scope="module")
def state_to_test():
    config_file = 'unit_tests/test_configurations/arena_pos_test_config.json'
    agents, engine = start_session(config_file, save=False, run=False)
    game_state = engine.get_state()
    return game_state


def test_debug():
    assert os.environ['DEBUG'] == 'True'


def test_all_arena_agents(state_to_test):
    agent_path = "battleground/games/arena/agents/"
    all_agent_paths = glob.glob(os.path.join(agent_path, '*.py'))

    assert len(all_agent_paths) > 0

    for agent_path in all_agent_paths:
        agent_path = agent_path.replace('/', '.')
        agent_path = agent_path[:-3]
        if '__' not in agent_path:
            agent = DynamicAgent('test', 'test', save=False, local_path=agent_path)
            move = agent.move(state_to_test)
            assert isinstance(move, dict)
            assert 'type' in move


def test_inital_db_agents(state_to_test):
    config_file = "battleground/config/initial_db_agents.json"

    with open(config_file, 'r') as file:
        agent_config_dict = json.load(file)

    print(agent_config_dict)
    for name, agent in agent_config_dict.items():
        print(name)
        agent = DynamicAgent(agent['name'],
                             agent['owner'],
                             save=False,
                             local_path=agent['local_path'])
        move = agent.move(state_to_test)
        assert isinstance(move, dict)
