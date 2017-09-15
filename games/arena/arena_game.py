from battleground.game_engine import GameEngine

from games.arena.calc import *
from games.arena.dungeon import Dungeon
from games.arena.event import Event
from games.arena.gladiator import Gladiator

import bisect
import random


class ArenaGameEngine(GameEngine):
    """
    An arena game engine based on an event queue.
    """
    def __init__(self, num_players, type, gladiator_stats=None, size=None, state=None):
        """
        :param num_players: int
        :param type: str
        :param gladiator_stats: list of dictionaries
                    each dict should have the form
                    { "pos": [int, int],
                      "name": str,
                      "team": int,
                      "stats": {"str": int, "dex": int, "con": int},
                      "skills": {"melee": int, "eva": int, "speed": int},
                      # optional
                      "cur_hp": int,
                      "cur_sp": int,
                      "boosts": {"att": int, "eva": int, "dam": int, "prot": int, "speed": int}
                    }
        :param size: [[int, int], [int, int]]
        :param state: {"gladiators": list of Gladiators,
                       "dungeon": Dungeon,
                       "queue": (list) event_queue}
            initializing:
            self.num_players
            self.current_player
            self.type
        """
        super().__init__(num_players, type)
        if state is not None:
            self.state = state
        else:
            # set up state by first creating gladiators from specified list
            # if more gladiators are specified than needed, the rest is ignored.
            if gladiator_stats is None:
                gladiator_stats = []
            self.gladiators = [Gladiator(pos=g["pos"],
                                         name=g["name"],
                                         team=g["team"],
                                         stats=g["stats"],
                                         skills=g["skills"])
                               for g in gladiator_stats[0:num_players]]
            if size is None:
                if len(gladiator_stats) > 0:
                    positions = [g.pos for g in self.gladiators]
                    pos_x = [p[0] for p in positions]
                    pos_y = [p[1] for p in positions]
                    size = [[min(pos_x), max(pos_x)], [min(pos_y), max(pos_y)]]
                else:
                    size = [[0, 10], [0, 10]]
            # if less gladiators are specified than needed, more are created on random positions
            if len(gladiator_stats) < num_players:
                for _ in range(0, num_players - len(gladiator_stats)):
                    # find free position
                    while True:
                        pos = [random.randint(size[0][0], size[0][1]),
                               random.randint(size[1][0], size[1][1])]
                        if all(pos != g.pos for g in self.gladiators):
                            break
                    self.gladiators.append(Gladiator(pos=pos))
            self.dungeon = Dungeon(size=size)
            # initialize event queue by sorting gladiators by their speed
            # returns list of tuples
            self.event_queue = sorted([(g.get_speed(),  # + calc.noise(),
                                        g) for g in self.gladiators],
                                      key=lambda event: event[0])
            self.state = {"gladiators": self.gladiators,
                          "dungeon": self.dungeon,
                          "queue": self.event_queue}

    def get_game_name(self):
        return self.type

    def get_state(self):
        return self.state

    def get_current_player(self):
        """
        This will be used by the game runner to determine which player should
        make the next move.
        The event_queue contains all events in occurring order. The move() function
        handles all non-player events and returns a state where next player is at the
        start of the event_queue.
        :returns index of first gladiator in event_queue in gladiators list
        """
        return self.gladiators.index(self.event_queue[0][1])

    def reset(self):
        """
        Initialize the game to the starting point
        """
        self.gladiators = [g.reset() for g in self.gladiators]
        self.event_queue = sorted([(g.get_speed(),  # + calc.noise(),
                                    g) for g in self.gladiators],
                                  key=lambda event: event[0])
        self.state = {"gladiators": self.gladiators,
                      "dungeon": self.dungeon,
                      "queue": self.event_queue}
        return None

    def within_bounds(self, pos):
        return bool(self.dungeon.size[0][0] < pos[0] < self.dungeon.size[0][1]
                and self.dungeon.size[1][0] < pos[1] < self.dungeon.size[1][1])

    def get_move_names(self, gladiator):
        """
        Used by agent to get available moves
        :param gladiator: Gladiator
        :return:
        """
        names = ["stay"]
        targets = self.get_targets(gladiator)
        if len(targets["move"]) > 0:
            names.append("move")
        if len(targets["attack"]) > 0:
            names.append("attack")
        if gladiator.cur_sp > 0:
            names.append("boost")
        return names

    def get_targets(self, gladiator):
        """
        Used by agent to get available targets.
        :param gladiator: Gladiator
        :return: (dict) of targets
        """
        directions = [[1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1], [0, -1], [1, -1]]
        targets = {"stay": [[0,0]],
                   "move": [d for d in directions
                            if self.within_bounds(gladiator.pos + d)],
                   "attack": [g for g in self.gladiators
                              if dist(gladiator.pos, g.pos) <= gladiator.range
                                 and g is not gladiator],
                   "boost": [k for k,v in gladiator.boosts.items()]
                   }
        return targets

    def get_values(self, gladiator):
        """
        Used by agent to get available values.
        :param gladiator: Gladiator
        :return: (dict) of values
        """
        values = {"stay": [1/s for s in range(1, gladiator.get_speed() + 1)],
                  "move": 0,
                  "attack": 0,
                  "boost": [sp for sp in range(1, gladiator.max_sp + 1)
                            if gladiator.get_cost("boost", sp) <= gladiator.cur_sp]
                  }
        return values

    def move(self, move):
        """
        Do a move on behalf of the current player.
        Go through event_queue handling all events until getting to next player.
        :param move: dict {"name": str of name of move,
                           "target": Gladiator or position [int, int] or (str) attribute,
                           "value": int
        :return:
        """
        assert "name" in move
        assert "target" in move
        assert "value" in move

        name = move["name"]
        target = move["target"]
        value = move["value"]

        (time, glad) = self.event_queue.pop(0)

        glad_event_time = time + glad.get_cost(name, value)  # + calc.noise()
        glad_event = Event(owner=glad,
                      time_stamp=glad_event_time,
                      type=name,
                      origin=glad.pos,
                      target=target,
                      value=value)
        if name is not "stay":
            bisect.insort(self.event_queue, (glad_event_time, glad_event))
        bisect.insort_right(self.event_queue, (glad_event_time, glad))

        if isinstance(self.event_queue[0][1], Event):
            (event_time, event) = self.event_queue.pop(0)

            while isinstance(event, Event):
                # handle events
                if event.name is "attack":
                    # attack function is checking if target is within range
                    event.target.chp -= event.owner.attack(event.target)
                    # go through event_queue in reversed order to keep items
                    # from changing index by deleting items with lower index
                    index = len(self.event_queue) - 1
                    for _, ev in reversed(self.event_queue):
                        # if gladiator is dead, delete it and all of his queued events.
                        if (isinstance(ev, Gladiator) and ev.chp <= 0
                            or isinstance(ev, Event) and ev.owner.chp <= 0):
                            del self.event_queue[index]
                        index -= 1

                elif event.name is "move":
                    blocked = False
                    for glad in self.gladiators:
                        if glad.pos == [x + y for x, y in zip(event.owner.pos, event.target)]:
                            blocked = True
                    if not blocked:
                        event.owner.move(event.target)

                elif event.name is "boost":
                    event.owner.set_boosts(event.target, event.value)

                (event_time, event) = self.event_queue.pop(0)

        # shrink dungeon
        positions = [g.pos for g in self.gladiators]
        pos_x = [p[0] for p in positions]
        pos_y = [p[1] for p in positions]
        self.dungeon.size = [[min(pos_x), max(pos_x)], [min(pos_y), max(pos_y)]]

        self.current_player = self.get_current_player()

        return None

    def game_over(self):
        """
        Check if the game is over
        """
        num_glads = sum([1 for g in self.event_queue if isinstance(g, Gladiator)])
        return bool(num_glads <= 1)
