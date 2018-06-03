import pytest
from battleground.games.arena.agents import random_walker, attacker
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

    assert len(game_state['move_options']) > 0

    walk_options = [x for x in game_state['move_options'] if x['type'] == 'move']
    move = rw.move(game_state)

    assert len(walk_options) > 0
    assert move['type'] == 'move'
    assert move['target'] in walk_options[0]['targets']


def test_arena_move(agents_and_engines):
    """test that game state updates appropriately"""
    agents, engine = agents_and_engines
    assert len(agents) == 3

    game_state = engine.get_state()

    positions = [g['pos'] for g in game_state['gladiators']]

    rw = random_walker.ArenaAgent()

    move = rw.move(game_state)
    for i in range(3):
        engine.move(move)
    new_state = engine.get_state()

    new_positions = [g['pos'] for g in new_state['gladiators']]

    assert new_positions != positions


def test_attacker(agents_and_engines):
    agents, engine = agents_and_engines
    assert len(agents) == 3

    game_state = engine.get_state()
    ra = attacker.ArenaAgent()

    attack_options = [x for x in game_state['move_options'] if x['type'] == 'attack']

    if len(attack_options) == 0:
        attack_options = {'type': 'attack', 'targets': [1]}
        game_state['move_options'].append(attack_options)
    else:
        attack_options = attack_options[0]

    move = ra.move(game_state)

    assert move['type'] == 'attack'
    assert move['target'] in attack_options['targets']
