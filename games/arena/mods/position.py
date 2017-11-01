
from games.arena.arena_game import *
from games.arena.dungeon import *
from games.arena.event import *
from games.arena.gladiator import *
from games.arena import calc

import random


class ArenaGameEngine(ArenaGameEngine):
    def __init__(self, state=None, *args, **kwargs):
        """
        :param state: {"dungeon": {"size": int},
                       ...}
        """
        super().__init__(self, state=state, *args, **kwargs)
        # is redefining init_gladiators also changing behavior for __init__ now?
        if state is not None and "dungeon" in state and "size" in state["dungeon"]:
            size = state["dungeon"]["size"]
        else:
            size = self.get_dungeon_size(self.gladiators)
        self.dungeon = Dungeon(size=size)

    def init_gladiators(self, num_players, gladiator_stats):
        """
        :param num_players: int
        :param gladiator_stats: list of dicts, see __init__
        :return: list of Gladiator objects
        """
        if gladiator_stats is None:
            gladiator_stats = []
        gladiators = [Gladiator(**g) for g in gladiator_stats[0:num_players]]
        # if less gladiators are specified than needed, more are created on random positions
        if len(gladiator_stats) < num_players:
            # This could potentially lead to a misbehavior when more gladiators
            # need to be added than free squares are available!
            if len(gladiator_stats) > 0:
                size = self.get_dungeon_size(gladiators)
            else:
                size = ((0, 2), (0, 2))
            for _ in range(0, num_players - len(gladiator_stats)):
                # find free position
                while True:
                    pos = (random.randint(size[0][0], size[0][1]),
                           random.randint(size[1][0], size[1][1]))
                    if all(pos != g.pos for g in gladiators):
                        break
                gladiators.append(Gladiator(pos=pos))
        return gladiators

    @staticmethod
    def get_dungeon_size(gladiators):
        positions = [g.pos for g in gladiators]
        pos_x = [p[0] for p in positions]
        pos_y = [p[1] for p in positions]
        size = ((min(pos_x) - 1, max(pos_x) + 1),
                (min(pos_y) - 1, max(pos_y) + 1))
        return size

    @staticmethod
    def within_bounds(pos, size):
        return bool(size[0][0] <= pos[0] <= size[0][1]
                    and size[1][0] <= pos[1] <= size[1][1])

    def get_move_options(self, gladiator_index):
        """
        Used by agent to get available moves
        :param gladiator_index: index in gladiators list
        :return: (dict) {name: {target: value}}
        """
        gladiator = self.gladiators[gladiator_index]
        options = super().get_move_options(self, gladiator_index)

        # add options for "move"
        directions = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
        targets = [d for d in directions
                   if self.within_bounds(calc.add_tuples(gladiator.pos, d),
                                         self.dungeon.size)]
        default_values = [None]
        if len(targets) > 0:
            options["move"] = {t: default_values for t in targets}

        # add options for "attack"
        # targets are indices of gladiators list
        targets = [self.gladiators.index(g) for g in self.gladiators
                   if (calc.dist(gladiator.pos, g.pos) <= gladiator.range
                       and not g.is_dead()
                       and g is not gladiator)]
        default_values = [None]
        if len(targets) > 0:
            options["attack"] = {t: default_values for t in targets}

        return options

    def handle_event(self, event):
        if event.type is "move":
            self.move_move(event)
        else:
            super().handle_event(self, event)

        self.dungeon.shrink_dungeon(self.state)
        return None

    def move_move(self, event):
        """
        Moves owner of event by target vector (if space is free.)
        :param event:
        :return:
        """
        blocked = False
        # for glad in self.gladiators:
        #    if glad.pos == calc.add_tuples(event.owner.pos, event.target):
        #        blocked = True
        if not blocked:
            self.gladiators[event.owner].move(event.target)
        return None


class Dungeon(Dungeon):
    def __init__(self, size, *args, **kwargs):
        """
        :param size: ((int, int), (int, int))
        """
        super().__init__(self, *args, **kwargs)
        self.size = size

    def get_init(self):
        init = super().get_init(self)
        init["size"] = self.size
        return init

    def shrink_dungeon(self, state):
        # shrink dungeon
        positions = [g.pos for g in state["gladiators"]]
        pos_x = [p[0] for p in positions]
        pos_y = [p[1] for p in positions]
        self.size = ((min(pos_x), max(pos_x)), (min(pos_y), max(pos_y)))
        return None


class Event(Event):
    def __init__(self, origin=None, *args, **kwargs):
        """
        :param owner: (int) gladiator index
        :param time_stamp: (float)
        :param type: (str) name of type of event
        :param target: (int) Gladiator index OR (int, int) position
        :param origin: (int, int) position
        """
        super().__init__(self, *args, **kwargs)
        self.origin = origin

    def get_init(self):
        init = super().get_init(self)
        init["origin"] = self.origin
        return init


class Gladiator(Gladiator):
    def __init__(self, pos, *args, **kwargs):
        """
        :param pos: (int, int)
        """
        super().__init__(self, *args, **kwargs)
        self.pos = pos
        self.range = 1

    def get_init(self):
        init = super().get_init(self)
        init["pos"] = self.pos
        init["range"] = self.range
        return init

    def attack(self, target):
        """
        :param target: object that has a position, evasion score and protection tuple
        :return: (int) damage
        """
        pos_o = self.pos
        pos_t = target.pos
        if calc.dist(pos_o, pos_t) > self.range:
            return 0
        else:
            return super().attack(self, target)

    def move(self, direction):
        """
        :param direction: (int, int) direction vector (list)
        :return: None
        """
        self.pos = calc.add_tuples(self.pos, direction)
        return None

    def get_cost(self, action, value):
        """
        :param action: (str)
        :param target: NotImplemented
        :param value: (int)
        :return: (int) cost in turn counts of a given action, given its target and value.
        """
        if action == "move":
            cost = self.get_speed()
        else:
            cost = super().get_cost(self, action, value)
        return int(cost)
