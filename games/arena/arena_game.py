from battleground.game_engine import GameEngine

from games.arena import calc
from games.arena.dungeon import Dungeon
from games.arena.event import Event
from games.arena.gladiator import Gladiator


class ArenaGameEngine(GameEngine):
    """
    An arena game engine based on an event queue.
    """

    def __init__(self, num_players, type="Arena", modules=None, state=None):
        """
        :param num_players: int
        :param type: str
        :param modules: list
        :param state: {"gladiators": list of gladiator_stats (see Gladiator class),
                       "dungeon": {},
                       "queue": (list) event_queue,
                       "scores: (dict)}
            initializing:
            self.num_players
            self.current_player
            self.type
        """
        super().__init__(num_players, type)
        if state is not None and "gladiators" in state:
            stats = state["gladiators"]
        else:
            stats = None
        self.gladiators = self.init_gladiators(num_players=num_players,
                                               gladiator_stats=stats)
        self.dungeon = Dungeon()
        if state is not None and "queue" in state:
            self.event_queue = [(t, self._init_event(e)) for t, e in state["queue"]]
        else:
            self.event_queue = sorted([(g.get_initiative(),  # + calc.noise(),
                                        self._init_event(g))
                                       for g in self.gladiators],
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
            for _ in range(0, num_players - len(gladiator_stats)):
                gladiators.append(Gladiator())
        return gladiators

    def _init_event(self, event):
        if isinstance(event, Gladiator):
            return Event(owner=self.gladiators.index(event),
                         type="gladiator")
        return Event(**event)

    def get_game_name(self):
        return self.type

    def get_state(self):
        return {"gladiators": [g.get_init() for g in self.gladiators],
                "dungeon": self.dungeon.get_init(),
                "queue": [(t, e.get_init()) for t, e in self.event_queue],
                "scores": self.scores
                }

    def get_current_player(self):
        """
        This will be used by the game runner to determine which player should
        make the next move.
        The event_queue contains all events in occurring order. The move() function
        handles all non-player events and returns a state where next player is at the
        start of the event_queue.
        :returns index of first gladiator in event_queue in gladiators list
        """
        return self.event_queue[0][1].owner

    def reset(self):
        """
        Initialize the game to the starting point
        """
        [g.reset() for g in self.gladiators]
        self.dungeon.reset()
        self.event_queue = sorted([(g.get_initiative(),  # + calc.noise(),
                                    self._init_event(g))
                                   for g in self.gladiators],
                                  key=lambda event: event[0])
        self.scores = {i: 0 for i in range(len(self.gladiators))}
        self.state = {"gladiators": self.gladiators,
                      "dungeon": self.dungeon,
                      "queue": self.event_queue,
                      "scores": self.scores
                      }
        return None

    def get_move_options(self, gladiator_index):
        """
        Used by agent to get available moves
        :param gladiator_index: index in gladiators list
        :return: (dict) {name: {target: value}}
        """
        gladiator = self.gladiators[gladiator_index]
        options = {}
        # add options for "stay"
        speed = gladiator.get_speed()
        options["stay"] = {None: [1]}  # [s / speed  for s in range(1, speed + 1)]}

        # add options for "attack"
        # targets are indices of gladiators list
        targets = [self.gladiators.index(g) for g in self.gladiators
                   if (not g.is_dead() and g is not gladiator)]
        default_values = [None]
        if len(targets) > 0:
            options["attack"] = {t: default_values for t in targets}

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

        while self.event_queue[0][1].type is not "gladiator":
            (event_time, event) = self.event_queue.pop(0)
            self.handle_event(event)

        self.current_player = self.get_current_player()
        return None

    def handle_event(self, event):
        if event.type is "stay":
            pass
        elif event.type is "attack":
            self.move_attack(event)
        else:
            pass
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

        (time, glad_event) = self.event_queue.pop(0)
        glad_index = glad_event.owner
        glad = self.gladiators[glad_index]
        event_queue_keys = [ev[0] for ev in self.event_queue]

        event_time = time + glad.get_cost(name, value)  # + calc.noise()

        event = Event(owner=glad_index,
                      type=name,
                      target=target,
                      value=value)
        if name is not "stay":
            calc.insort_right(self.event_queue,
                              event_queue_keys,
                              (event_time, event),
                              keyfunc=lambda e: e[0])

        next_glad_event = Event(owner=glad_index,
                                type="gladiator",
                                target=None,
                                value=None)
        calc.insort_right(self.event_queue,
                          event_queue_keys,
                          (event_time, next_glad_event),
                          keyfunc=lambda e: e[0])
        return None

    def move_attack(self, event):
        """
        Owner attacks target. If target dies, it's removed from event_queue
        :param event:
        :return: None
        """
        target = self.gladiators[event.target]
        attacker = self.gladiators[event.owner]
        # attack function is checking if target is within range
        target.cur_hp -= attacker.attack(target)
        # go through event_queue in reversed order to keep items
        # from changing index by deleting items with lower index
        index = len(self.event_queue) - 1
        for _, ev in reversed(self.event_queue):
            # if gladiator is dead, delete it and all of his queued events.
            if self.gladiators[ev.owner].cur_hp <= 0:
                del self.event_queue[index]
                # Each kill gives one score point, dying sets score to zero.
                if ev.type is "gladiator":
                    self.state["scores"][ev.owner] = 0
                    self.state["scores"][event.owner] += 1
            index -= 1
        return None

    def game_over(self):
        """
        Check if the game is over
        """
        num_glads = sum([1 for (t, g) in self.event_queue if g.type is "gladiator"])
        return bool(num_glads <= 1)
