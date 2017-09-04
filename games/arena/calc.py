"""
calculation module for arena_game
"""

import random


def dist(pos_a, pos_b):
    """
    :param pos_a:
    :param pos_b:
    :returns L_1 distance between positions
    """
    dist_x = abs(pos_a[0] - pos_b[0])
    dist_y = abs(pos_a[1] - pos_b[1])
    return max(dist_x, dist_y)


def noise():
    """
    noise function for solving clash in sorting of event_queue
    """
    return random.randint(1, 999) / 1000
