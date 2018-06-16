import pytest
from battleground.dynamic_agent import DynamicAgent
from battleground.site_runner import start_session
import glob
import os.path


@pytest.fixture(scope="module")
def state_to_test():
    config_file = 'unit_tests/test_configurations/arena_pos_test_config.json'
    agents, engine = start_session(config_file, save=False, run=False)
    game_state = engine.get_state()
    return game_state


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
