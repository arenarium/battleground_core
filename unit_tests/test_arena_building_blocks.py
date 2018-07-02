import pytest
from battleground.games.arena import building_blocks
from battleground.site_runner import start_session
import copy


@pytest.fixture(scope="module")
def states_to_test():
    config_file = 'unit_tests/test_configurations/arena_pos_test_config.json'
    agents, engine = start_session(config_file, save=False, run=False)
    game_state = engine.get_state()

    attack_options = []

    for option in game_state['move_options']:
        if 'type' in option and 'targets' in option:
            if option['type'] == 'attack' and option['targets'] != [game_state['current_player']]:
                attack_options.append(option)

    if len(attack_options) == 0:
        other = building_blocks.closest_other(game_state)
        attack_options = [{'type': 'attack', 'targets': [other]}]

    other_options = [o for o in game_state['move_options'] if o['type'] != 'attack']

    game_state_with_attack = copy.deepcopy(game_state)
    game_state_with_attack['move_options'] = attack_options + other_options

    game_state_without_attack = copy.deepcopy(game_state)
    game_state_without_attack['move_options'] = other_options

    return game_state_without_attack, game_state_with_attack


def test_closest_other(states_to_test):
    for state in states_to_test:
        other = building_blocks.closest_other(state)
        assert isinstance(other, int)
        assert other != state['current_player']


def test_attack(states_to_test):
    state_without_attack, state_with_attack = states_to_test
    move_options = state_with_attack['move_options']
    attack_options = [o for o in move_options if o['type'] == 'attack'][0]
    move = building_blocks.attack(state_with_attack, attack_options['targets'][0])

    assert isinstance(move, dict)


def test_others(states_to_test):
    for state in states_to_test:
        others = building_blocks.others(state)
        assert isinstance(others, dict)
        assert len(others) == len(state['gladiators']) - 1


def test_move(states_to_test):

    xx = [-1, 0, 1.0, 100]
    yy = [-1, -100, 0.5, 5]
    for x in xx:
        for y in yy:
            loc = (x, y)
            for state in states_to_test:
                move = building_blocks.move_toward(state, loc)
                assert isinstance(move, dict)
                assert 'type' in move
                assert move['type'] == 'move'
                assert len(move['target']) > 0


def test_distances():
    xx = [-1, 0, 1.0, 100]
    yy = [-1, -100, 0.5, 5]
    for x in xx:
        for y in yy:
            reference_location = (x, y)
            other_locations = list(zip(xx, yy))
            distances = building_blocks.distances(reference_location, other_locations)
            assert all([d >= 0 for d in distances])

            for d, ol in zip(distances, other_locations):
                d_ = sum([(x-y)**2 for x, y in zip(reference_location, ol)])**0.5
                assert d == pytest.approx(d_)


def test_attack_closest(states_to_test):
    state_without_attack, state_with_attack = states_to_test

    print(state_with_attack)

    move = building_blocks.attack_closest(state_with_attack)
    assert isinstance(move, dict)
    assert 'type' in move
    assert move['type'] == 'attack'

    move = building_blocks.attack_closest(state_without_attack)
    assert move is None


def test_random_walk(states_to_test):
    state_without_attack, state_with_attack = states_to_test
    for state in states_to_test:
        move = building_blocks.random_walk(state)
        assert 'type' in move
        assert move['type'] == 'move'
