import copy

from battleground.game_engine import GameEngine
from games.arena import calc
from games.arena.dungeon import Dungeon
from games.arena.event import Event
from games.arena.gladiator import Gladiator


class ArenaGameEngine(GameEngine):
    """
    An arena game engine based on an event queue.
    """

    dungeon_class = Dungeon
    event_class = Event
    gladiator_class = Gladiator

    def __init__(self, num_players=2, type="Arena", state=None):
        """
        :param num_players: int
        :param type: str
        :param state: {"gladiators": list of gladiator_stats (see Gladiator class),
                       "dungeon": {},
                       "queue": (list) event_queue,
                       "scores: (dict)}
            initializing:
            self.num_players
            self.current_player
            self.type
        """
        super().__init__(num_players=num_players, type=type)

        # init gladiators
        if state is not None \
                and "gladiators" in state:
            stats = state["gladiators"]
        else:
            stats = []
        self.gladiators = [self.gladiator_class(**g) for g in stats[0:num_players]]

        if len(stats) < num_players:
            for _ in range(0, num_players - len(stats)):
                new_stats = self.init_new_gladiator_stats(self.gladiators)
                self.gladiators.append(self.gladiator_class(**new_stats))

        # init dungeon
        if state is not None \
                and "dungeon" in state:
            dungeon_stats = state["dungeon"]
        else:
            dungeon_stats = self.init_new_dungeon_stats(self.gladiators)
        self.dungeon = self.dungeon_class(**dungeon_stats)

        # init event_queue
        if state is not None \
                and "queue" in state:
            self.event_queue = [(t, self._init_event(e)) for t, e in state["queue"]]
        else:
            self.event_queue = sorted([(g.get_initiative(),  # + calc.noise(),
                                        self._init_event(g))
                                       for g in self.gladiators],
                                      key=lambda event: event[0])

        # init scores
        if state is not None \
                and "scores" in state:
            self.scores = state["scores"]
        else:
            self.scores = {i: 0 for i in range(num_players)}

        # init state
        self.state = {"gladiators": self.gladiators,
                      "dungeon": self.dungeon,
                      "queue": self.event_queue,
                      "scores": self.scores
                      }

    def init_new_gladiator_stats(self, *args, **kwargs):
        """
        :return: list of stats to create Gladiator object at start of the game
        """
        return {}

    def init_new_dungeon_stats(self, *args, **kwargs):
        """
        :return: list of stats to create Dungeon object at start of the game
        """
        return {}

    def _init_event(self, event):
        """
        Instantiates an Event of type "gladiator" if event is a Gladiator instance
        or, if event is a dict, using its keys to instantiate an Event with those parameters.
        :param event: EITHER Gladiator OR dict
        :return: Event instance
        """
        if isinstance(event, self.gladiator_class):
            return self.event_class(owner=self.gladiators.index(event),
                                    type="gladiator")
        return self.event_class(**event)

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
        :return: None
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
        self.queue_move(move)

        while self.event_queue[0][1].type is not "gladiator":
            (event_time, event) = self.event_queue.pop(0)
            queue_copy = copy.deepcopy(self.event_queue)
            self.handle_event(event)
            self.update_scores(player=event.owner, old_queue=queue_copy)

        self.current_player = self.get_current_player()
        return None

    def handle_event(self, event):
        """
        :param event:
        :return: None
        """
        if event.type is "stay":
            pass
        elif event.type is "attack":
            self.move_attack(event)
        else:
            pass
        return None

    def queue_move(self, move):
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

        event_time = time + glad.get_cost(action=name, target=target, value=value)  # + calc.noise()

        event = self.event_class(owner=glad_index,
                                 type=name,
                                 target=target,
                                 value=value)
        calc.insort_right(self.event_queue,
                          event_queue_keys,
                          (event_time, event),
                          keyfunc=lambda e: e[0])
        next_glad_event = self.event_class(owner=glad_index,
                                           type="gladiator")
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
        target.cur_hp -= attacker.attack(target)
        self.remove_dead()
        return None

    def remove_dead(self):
        """
        Removes events of gladiators that are dead.
        :return: None
        """
        # go through event_queue in reversed order to keep items
        # from changing index by deleting items with lower index
        index = len(self.event_queue) - 1
        for _, ev in reversed(self.event_queue):
            # if gladiator is dead, delete it and all of its queued events.
            if self.gladiators[ev.owner].is_dead():
                del self.event_queue[index]
            index -= 1
        return None

    def update_scores(self, player, old_queue):
        """
        Updates scores of player based on difference between old_queue and self.event_queue.
        It is assumed that all these changes are due to player.
        :param player: (int) player index
        :param old_queue: event_queue before event(s) happened
        :return: None
        """
        # get all events that were removed from event_queue
        queue_complement = set(old_queue) - set(self.event_queue)
        for _, ev in queue_complement:
            # Each kill gives one score point, dying sets score to zero.
            if ev.type is "gladiator":
                self.state["scores"][ev.owner] = 0
                self.state["scores"][player] += 1
        return None

    def game_over(self):
        """
        Check if the game is over
        :return: (bool)
        """
        num_glads = sum([1 for (t, g) in self.event_queue if g.type is "gladiator"])
        return bool(num_glads <= 1)
