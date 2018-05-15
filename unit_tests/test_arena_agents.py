import pytest
from battleground.games.arena.agents import random_walker
from battleground.site_runner import start_session


@pytest.fixture(scope="module")
def agents_and_engines():
    config_file = 'unit_tests/test_configurations/arena_pos_test_config.json'
    return start_session(config_file, save=False, run=False)


def test_random_walker(agents_and_engines):
    agents, engine = agents_and_engines
    assert len(agents) == 3

    game_state = engine.get_state()
    rw = random_walker.ArenaAgent()

    walk_options = [x for x in game_state['move_options'] if x['type'] == 'move'][0]

    move = rw.move(game_state)
    assert move['type'] == 'move'

    assert move['target'] in walk_options['targets']
