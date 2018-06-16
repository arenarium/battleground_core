"""
calculation module for arena_game
"""

from bisect import bisect_right
import random


def argmin(iterable):
    return min(enumerate(iterable), key=lambda x: x[1])[0]


def argmin_dict(d):
    return min(d.items(), key=lambda x: x[1])[0]


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
    :returns (float) in [0.001, 0.999]
    """
    return random.randint(1, 999) / 1000


def insort_right(seq, keys, item, keyfunc):
    """ https://stackoverflow.com/questions/27672494/how-to-use-bisect-insort-left-with-a-key
        Insert an item into the sorted list using separate corresponding
        keys list and a keyfunc to extract key from each item.
    """
    key = keyfunc(item)  # get key
    index = bisect_right(keys, key)  # determine where to insert item
    keys.insert(index, key)  # insert key of item in keys list
    seq.insert(index, item)  # insert the item itself in the corresponding spot
    return None


def move_options_to_list(move_options):
    """
    :param move_options: from get_move_options(gladiator_index)
    :return: list of move options, from which an agent can directly select
    """
    options_list = []
    option = []

    def to_dict(list_of_tuples):
        return {t[0]: t[1] for t in list_of_tuples}

    def options_culling(arg):
        if isinstance(arg, list):
            for element in arg:
                options_culling(element)
                del option[-1]
        elif isinstance(arg, dict):
            # the dict is unordered, but we first need to cull the description of the option
            # before nesting further. The dict has len == 2, so it's cheap.
            for k, v in arg.items():
                if not isinstance(v, list):
                    option.append((k, v))
            for k, v in arg.items():
                if isinstance(v, list):
                    if isinstance(v[0], dict):  # v is list of dicts
                        options_culling(v)
                    else:  # v is list of values
                        # they keys are strings, and for the last list of options they are given as
                        #   'values': [ ... ]
                        # removing the plural 's' gives the singular
                        # form which appears in the move dict
                        # ASSUMPTION: A KEY THAT ENDS ON 's' IS IN PLURAL FORM
                        if k[-1] is 's':
                            key = k[:-1]
                        else:
                            key = k
                        for value in v:
                            option.append((key, value))
                            options_list.append(to_dict(option))
                            del option[-1]
        else:  # will never be reached
            option.append(arg)
            options_list.append(to_dict(option))
            del option[-1]
        return None

    options_culling(move_options)
    return options_list
