from battleground.game_engine import GameEngine

from games.arena import calc
from games.arena.dungeon import Dungeon
from games.arena.event import Event
from games.arena.gladiator import Gladiator

import random


class ArenaGameEngine(GameEngine):
    """
    An arena game engine based on an event queue.
    """

    def __init__(self, num_players, type,
                 gladiator_stats=None, size=None, state=None):
        """
        :param num_players: int
        :param type: str
        :param gladiator_stats: list of dictionaries
                    each dict should have the form
                    { "pos": (int, int),
                      "name": str,
                      "team": int,
                      "stats": {"str": int, "dex": int, "con": int},
                      "skills": {"melee": int, "eva": int, "speed": int},
                      # optional
                      "cur_hp": int,
                      "cur_sp": int,
                      "boosts": {"att": int, "eva": int, "dam": int, "prot": int, "speed": int}
                    }
        :param size: ((int, int), (int, int))
        :param state: {"gladiators": list of Gladiators,
                       "dungeon": Dungeon,
                       "queue": (list) event_queue,
                       "scores: (dict)}
            initializing:
            self.num_players
            self.current_player
            self.type
        """
        super().__init__(num_players, type)
        if state is not None and "gladiators" in state:
            self.gladiators = state["gladiators"]
        else:
            self.gladiators = self._init_gladiators(num_players=num_players,
                                                    gladiator_stats=gladiator_stats)
        if state is not None and "dungeon" in state:
            self.dungeon = state["dungeon"]
        else:
            if size is None:
                size = self._get_dungeon_size(self.gladiators)
            self.dungeon = Dungeon(size=size)
        if state is not None and "queue" in state:
            self.event_queue = state["queue"]
        else:
            self.event_queue = sorted([(g.get_speed(),  # + calc.noise(),
                                        g) for g in self.gladiators],
                                      key=lambda event: event[0])
        if state is not None and "scores" in state:
            self.scores = state["scores"]
        else:
            self.scores = {i: 0 for i in range(num_players)}

        self.state = {"gladiators": self.gladiators,
                      "dungeon": self.dungeon,
                      "queue": self.event_queue,
                      "scores": self.scores
                      }

    def _init_gladiators(self, num_players, gladiator_stats):
        """
        :param num_players: int
        :param gladiator_stats: list of dicts, see __init__
        :return: list of Gladiator objects
        """
        if gladiator_stats is None:
            gladiator_stats = []
        gladiators = [Gladiator(pos=g["pos"],
                                name=g["name"],
                                team=g["team"],
                                stats=g["stats"],
                                skills=g["skills"])
                      for g in gladiator_stats[0:num_players]]
        # This could potentially lead to a misbehavior when more gladiators
        # need to be added than free squares are available!
        if len(gladiator_stats) > 0:
            size = self._get_dungeon_size(gladiators)
        else:
            size = ((0, 2), (0, 2))
        # if less gladiators are specified than needed, more are created on random positions
        if len(gladiator_stats) < num_players:
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
    def _get_dungeon_size(gladiators):
        positions = [g.pos for g in gladiators]
        pos_x = [p[0] for p in positions]
        pos_y = [p[1] for p in positions]
        size = ((min(pos_x)-1, max(pos_x)+1),
                (min(pos_y)-1, max(pos_y)+1))
        return size

    def get_game_name(self):
        return self.type

    def get_state(self):
        return self.state

    @staticmethod
    def decode_state(state):
        return {"gladiators": [g.get_init() for g in state["gladiators"]],
                "dungeon": state["dungeon"].get_init(),
                "queue": [(t, e.get_init()) for t, e in state["queue"]],
                "scores": state["scores"]
                }

    @staticmethod
    def decode_move(move):
        name = move["name"]
        if isinstance(move["target"], Gladiator):
            target = move["target"].get_init()
        else:
            target = move["target"]
        value = move["value"]

        return {"name": name,
                "target": target,
                "value": value}

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
                      "queue": self.event_queue,
                      "scores": {i: 0 for i in range(len(self.gladiators))}
                      }
        return None

    @staticmethod
    def within_bounds(pos, size):
        return bool(    size[0][0] < pos[0] < size[0][1]
                    and size[1][0] < pos[1] < size[1][1])

    def get_move_options(self, gladiator):
        """
        Used by agent to get available moves
        :param gladiator: Gladiator
        :return: (dict) {name: {target: value}}
        """
        options = {}
        # add options for "stay"
        speed = gladiator.get_speed()
        options["stay"] = {(0, 0): [s / speed  for s in range(1, speed + 1)]}

        # add options for "move"
        directions = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
        targets = [d for d in directions
                   if self.within_bounds(calc.add_tuples(gladiator.pos, d),
                                         self.dungeon.size)]
        default_values = [0]
        if len(targets) > 0:
            options["move"] = {t: default_values for t in targets}

        # add options for "attack"
        targets = [g for g in self.gladiators
                   if calc.dist(gladiator.pos, g.pos) <= gladiator.range
                   and g is not gladiator]
        default_values = [0]
        if len(targets) > 0:
            options["attack"] = {t: default_values for t in targets}

        # add options for "boost"
        targets = {}
        for attr, val in gladiator.boosts.items():
            values = list(range(-gladiator.get_boost_cost(attr, val),
                                gladiator.cur_sp + 1))
            if len(values) > 0:
                targets[attr] = values
        if len(targets) > 0:
            options["boost"] = targets

        return options

    def move(self, move):
        """
        Execute a move on behalf of the current player.
        Go through event_queue handling all events until getting to next player.
        :param move: dict {"name": str of name of move,
                           "target": Gladiator or position (int, int) or (str) attribute,
                           "value": float
        :return:
        """
        self.move_queue(move)

        while isinstance(self.event_queue[0][1], Event):
            (event_time, event) = self.event_queue.pop(0)
            # handle events
            if event.type is "stay":
                pass
            elif event.type is "attack":
                self.move_attack(event)
            elif event.type is "move":
                self.move_move(event)
            elif event.type is "boost":
                self.move_boost(event)

        self.dungeon.shrink_dungeon(self.state)
        self.current_player = self.get_current_player()
        return None

    def move_queue(self, move):
        """
        Queue move and player into event_queue.
        :param move:
        :return: None
        """
        assert "name" in move
        assert "target" in move
        assert "value" in move

        name = move["name"]
        target = move["target"]
        value = move["value"]

        (time, glad) = self.event_queue.pop(0)
        event_queue_keys = [event[0] for event in self.event_queue]

        glad_event_time = time + glad.get_cost(name, value)  # + calc.noise()
        glad_event = Event(owner=glad,
                           time_stamp=glad_event_time,
                           type=name,
                           origin=glad.pos,
                           target=target,
                           value=value)
        if name is not "stay":
            calc.insort_right(self.event_queue,
                              event_queue_keys,
                              (glad_event_time, glad_event),
                              keyfunc=lambda e: e[0])
        calc.insort_right(self.event_queue,
                          event_queue_keys,
                          (glad_event_time, glad),
                          keyfunc=lambda e: e[0])
        return None

    def move_attack(self, event):
        """
        Owner attacks target. If target dies, it's removed from event_queue
        :param event:
        :return: None
        """
        # attack function is checking if target is within range
        event.target.cur_hp -= event.owner.attack(event.target)
        # go through event_queue in reversed order to keep items
        # from changing index by deleting items with lower index
        index = len(self.event_queue) - 1
        for _, ev in reversed(self.event_queue):
            # if gladiator is dead, delete it and all of his queued events.
            if (isinstance(ev, Gladiator) and ev.cur_hp <= 0
                or isinstance(ev, Event) and ev.owner.cur_hp <= 0):
                del self.event_queue[index]
                # Each kill gives one score point, dying sets score to zero.
                if isinstance(ev, Gladiator):
                    ind_loser = self.gladiators.index(ev)
                    self.state["scores"][ind_loser] = 0
                    ind_winner = self.gladiators.index(event.owner)
                    self.state["scores"][ind_winner] += 1
            index -= 1
        return None

    def move_move(self, event):
        """
        Moves owner of event by target vector (if space is free.)
        :param event:
        :return:
        """
        blocked = False
        #for glad in self.gladiators:
        #    if glad.pos == calc.add_tuples(event.owner.pos, event.target):
        #        blocked = True
        if not blocked:
            event.owner.move(event.target)
        return None

    @staticmethod
    def move_boost(event):
        """
        Boosts target of owner of event by event value.
        :param event:
        :return: None
        """
        if isinstance(event.target, list):
            targets = event.target
        else:
            targets = [event.target]
        if isinstance(event.value, list):
            values = event.value
        else:
            values = [event.value]
        boosts = dict(zip(targets, values))
        event.owner.set_boosts(boosts)
        return None

    def game_over(self):
        """
        Check if the game is over
        """
        num_glads = sum([1 for (t, g) in self.event_queue if isinstance(g, Gladiator)])
        return bool(num_glads <= 1)
