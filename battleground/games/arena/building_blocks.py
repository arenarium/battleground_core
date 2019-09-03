from . import util
import random
import numpy as np


def random_move(state, seppuku=True):
    move_options = util.move_options_to_list(state['move_options'])
    if not seppuku:
        myself = state["current_player"]
        move_options = [o for o in move_options
                        if not ("type" in o and "target" in o
                                and o["type"] is "attack" and o["target"] is myself)]
    if len(move_options) > 0:
        return random.choice(move_options)
    else:
        return {}


def random_walk(state):
    move_options = util.move_options_to_list(state['move_options'])
    walk_options = [o for o in move_options if o['type'] == 'move']
    if len(walk_options) > 0:
        return random.choice(walk_options)
    else:
        return {}


def closest_other(state):
    """
    Get the id of the closest other player.

    :param state: The current game state.
    :returns: (int) index in gladiator list.

    """
    locations = others_locations(state)
    distances_ = distances(my_location(state), list(locations.values()))
    dist_dict = {key: dist for key, dist in zip(locations, distances_)}
    target = util.argmin_dict(dist_dict)
    return target


def closest_other_location(state):
    """
    Get the location of the closest other player, e.g., (x, y).

    :param state: The current game state.
    :returns: tuple (x, y).

    """
    locations = others_locations(state)
    target = closest_other(state)
    return locations[target]


def others(state, alive=True):
    """
    Get a dictionary of other players.

    :param state: The current game state.
    :returns: (dict) {id: player data, ...}
    """
    me = state['current_player']
    all_players = state['gladiators']
    others = {i: g for i, g in enumerate(all_players) if i != me}

    if alive:
        others = {i: g for i, g in others.items() if g['cur_hp'] > 0}

    return others


def others_locations(state):
    """
    Get a dictionary of the locations of players, excluding the current player.

    :param state: The current game state.
    :returns: dict of locations, e.g., {id: (x, y), ...}.

    """
    others_ = others(state)
    locations = {i: e['pos'] for i, e in others_.items()}
    return locations


def my_location(state):
    """
    Get the location of the current player.

    :param state: The current game state.
    :returns: tuple (x, y)

    """
    return state['gladiators'][state['current_player']]['pos']


def distances(reference_location, locations):
    """
    Compute distances from a reference location to a set of other locations.

    :param reference_location: iterable of coordinates, e.g., (1, 2)
    :param locations: iterable of iterables of coordinates, e.g., [(0, 0), (2, 1), ...]

    :returns: dict of distances {id: float, ...}

    """
    differences = np.array(locations) - np.array(reference_location)
    distances_ = np.sqrt(np.sum(differences**2, axis=1))
    return distances_


def move_relative(state, location, towards):
    """
    Generate move that takes you most directly towards or away from
    the specified location.

    shorthand functions move_toward and move_away are available.

    :param state: The current game state.
    :param location: tuple of target position, e.g, (x, y)
    :param towards: bool, move towards location if true, away otherwise

    :returns: A move object (dict).

    """
    move_options = util.move_options_to_list(state['move_options'])

    move_options = [m for m in move_options if m['type'] == 'move']

    if len(move_options) == 0:
        return None

    my_location_ = my_location(state)
    move_targets = np.array([m['target'] for m in move_options])
    target_locations = move_targets + my_location_

    distances_ = distances(location, target_locations)

    if towards:
        target_index = np.argmin(distances_)
    else:
        target_index = np.argmax(distances_)

    return move_options[target_index]


def move_toward(state, location):
    """
    Generate move that takes you most directly to the specified location.

    :param state: The current game state.
    :param location: tuple of target position, e.g, (x, y)

    :returns: A move object (dict).

    """
    return move_relative(state, location, True)


def move_away(state, location):
    """
    Generate move that takes you most quickly away from the specified location.

    :param state: The current game state.
    :param location: tuple of target position, e.g, (x, y)

    :returns: A move object (dict).

    """

    return move_relative(state, location, False)


def attack(state, target):
    """
    Generate a move object to attack the target, if that is a valid move.
    Otherwise, return None.

    :param state: The current game state.
    :param target: id of the target.

    :returns: A move object (dict) or None

    """
    move_options = util.move_options_to_list(state['move_options'])

    proposed_move = {'type': 'attack', 'target': target}

    if proposed_move in move_options:
        return proposed_move
    else:
        return None


def attack_closest(state):
    """
    Generate a move object to attack the closest other player, if that is a valid move.
    Otherwise, return None.

    :param state: The current game state.
    :returns: A move object (dict), or None.

    """
    locations = others_locations(state)
    distances_ = distances(my_location(state), list(locations.values()))
    others_distances = {key: d for key, d in zip(locations.keys(), distances_)}
    target = util.argmin_dict(others_distances)

    return attack(state, target)


def attack_myself(state):
    """
    Generate a move object to attack yourself.

    :param state: The current game state.
    :returns: A move object (dict).

    """
    return attack(state, state['current_player'])


def my_hitpoints(state):
    """
    Return current health (hitpoints) of the player.

    :param state: The current game state.
    :returns: int.

    """
    return state['gladiators'][state['current_player']]['cur_hp']


def others_hitpoints(state):
    """
    Return current health (hitpoints) of other players.

    :param state: The current game state.
    :returns: dict(id: int).

    """
    others_ = others(state)

    return {i: g['cur_hp'] for i, g in others_.items()}
