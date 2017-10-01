"""
calculation module for arena_game
"""

from bisect import bisect_right
import random


def add_tuples(tuple_a, tuple_b):
    """
    :param tuple_a: ((int), (int))
    :param tuple_b: ((int), (int))
    :return: vector addition of tuple_a + tuple_b
    """
    return tuple([x + y for x, y in zip(tuple_a, tuple_b)])


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


def insort_right(seq, keys, item, keyfunc):
    """ https://stackoverflow.com/questions/27672494/how-to-use-bisect-insort-left-with-a-key
        Insert an item into the sorted list using separate corresponding
        keys list and a keyfunc to extract key from each item.
    """
    key = keyfunc(item)              # get key
    index = bisect_right(keys, key)  # determine where to insert item
    keys.insert(index, key)          # insert key of item in keys list
    seq.insert(index, item)          # insert the item itself in the corresponding spot
    return None

