
from battleground.game_engine import GameEngine
from . import util
from .dungeon import Dungeon
from .event import Event
from .gladiator import Gladiator

import random


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
        self.dungeon = None

        # init gladiators from exsisting game state, if provided
        if state is not None \
                and "gladiators" in state:
            stats = state["gladiators"]
        else:
            stats = []
        self.gladiators = [self.gladiator_class(**g)
                           for g in stats[0:num_players]]

        # create new players if number of specified players > existing players
        if len(stats) < num_players:
            for _ in range(0, num_players - len(stats)):
                new_stats = self.init_new_gladiator_stats(self.gladiators)
                self.gladiators.append(self.gladiator_class(**new_stats))

        # init dungeon
        if state is not None and "dungeon" in state:
            dungeon_stats = state["dungeon"]
        else:
            dungeon_stats = self.init_new_dungeon_stats(self.gladiators)
        self.dungeon = self.dungeon_class(**dungeon_stats)

        # init event_queue
        if state is not None and "queue" in state:
            self.event_queue = [(t, self._init_event(e)) for t, e in state["queue"]]
        else:
            self.event_queue = [(g.get_initiative(),  # + util.noise(),
                                 self._init_event(g))
                                for g in self.gladiators]
            # shuffle list to guarantee no advantage of one player over another
            # by always being first (at equal initiative)
            random.shuffle(self.event_queue)
            # sort by initiative
            self.event_queue = sorted(self.event_queue, key=lambda event: event[0])

        # init scores
        if state is not None \
                and "scores" in state:
            self.scores = state["scores"]
        else:
            self.scores = {i: 0 for i in range(num_players)}

        self.message = []

        # init state
        self.state = {"gladiators": self.gladiators,
                      "dungeon": self.dungeon,
                      "queue": self.event_queue,
                      "scores": self.scores,
                      "message": self.message
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

    def get_state(self, observer_id=None):
        """
        :return: (dict) parsed state
        """
        return {"gladiators": [g.get_init() for g in self.gladiators],
                "dungeon": self.dungeon.get_init(),
                "queue": [(t, e.get_init()) for t, e in self.event_queue],
                "scores": self.scores,
                "message": self.message,
                "move_options": self.get_move_options(self.get_current_player()),
                "current_player": self.get_current_player()
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
        for glad in self.gladiators:
            glad.reset()
        self.dungeon.reset()
        self.event_queue = sorted([(g.get_initiative(),  # + util.noise(),
                                    self._init_event(g))
                                   for g in self.gladiators],
                                  key=lambda event: event[0])
        self.scores = {i: 0 for i in range(len(self.gladiators))}
        self.state = {"gladiators": self.gladiators,
                      "dungeon": self.dungeon,
                      "queue": self.event_queue,
                      "scores": self.scores,
                      "message": self.message
                      }
        return None

    def get_move_options(self, gladiator_index):
        """
        Used by agent to get available moves
        :param gladiator_index: index in gladiators list
        :return: (dict) [{type: type,
                          tools: [{tool: tool,
                                   targets: [{target: target,
                                              values: [value]
                                              }
                                             ]
                                   }
                                  ]
                          }
                         ]
        """
        gladiator = self.gladiators[gladiator_index]
        options = []
        # add options for "stay"
        # speed = gladiator.get_speed()
        values = [1]  # [s / speed for s in range(1, speed + 1, int(speed / 3))]
        # values.append(1)
        options_stay = {"type": "stay",
                        "values": values
                        }
        options.append(options_stay)

        # add options for "attack"
        # targets are indices of gladiators list
        targets = [self.gladiators.index(g) for g in self.gladiators if not g.is_dead()]
        if targets:
            options_attack = {"type": "attack",
                              "targets": targets
                              }
            options.append(options_attack)

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

        # behaviour for bad move returned
        if not move or 'type' not in move:
            move = {}
            move['type'] = 'stay'
            move['value'] = 1

        self.queue_move(move)
        self.message = []

        while self.event_queue[0][1].type is not "gladiator":
            (_, event) = self.event_queue.pop(0)
            self.handle_event(event)
            if event.type is not "gladiator":
                self.message.append(("event", event.get_init()))

        self.current_player = self.get_current_player()
        return None

    def queue_move(self, move):
        """
        Queue move and player into event_queue.
        :param move:
        :return: None
        """
        (time, glad_event) = self.event_queue.pop(0)
        time = int(time)
        glad_index = glad_event.owner
        glad = self.gladiators[glad_index]
        event_queue_keys = [ev[0] for ev in self.event_queue]

        event_time = time + glad.get_cost(**move)  # + util.noise()
        event_stats = self.init_queued_event_stats(time=time,
                                                   glad_event=glad_event,
                                                   move=move)
        event = self.event_class(**event_stats)

        util.insort_right(self.event_queue,
                          event_queue_keys,
                          (event_time, event),
                          keyfunc=lambda e: e[0])
        next_glad_event = self.event_class(owner=glad_index,
                                           type="gladiator",
                                           time_stamp=time)
        util.insort_right(self.event_queue,
                          event_queue_keys,
                          (event_time, next_glad_event),
                          keyfunc=lambda e: e[0])
        return None

    def init_queued_event_stats(self, time, glad_event, move):
        """
        :param time: time the event is created
        :param glad_event: event the gladiator is called
        :param move: dict describing the move the gladiator wants to queue
        :return: dict of stats for instantiation of event.
        """
        stats = move
        stats["owner"] = glad_event.owner
        stats["time_stamp"] = time
        return stats

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

    def move_attack(self, event):
        """
        Owner attacks target. If target dies, it's removed from event_queue
        :param event:
        :return: None
        """
        target = self.gladiators[event.target]
        attacker = self.gladiators[event.owner]
        target.cur_hp -= attacker.attack(target)
        corpse_count = self.remove_dead()
        self.state["scores"][event.owner] += corpse_count
        if attacker.is_dead():
            self.state["scores"][event.owner] = 0
        return None

    def remove_dead(self):
        """
        Removes events of gladiators that are dead.
        :return: number of corpses
        """
        corpse_count = 0
        # go through event_queue in reversed order to keep items
        # from changing index by deleting items with lower index
        index = len(self.event_queue) - 1
        for _, event in reversed(self.event_queue):
            # if gladiator is dead, delete it and all of its queued events.
            if self.gladiators[event.owner].is_dead():
                # Dying sets score to zero.
                if event.type is "gladiator":
                    self.state["scores"][event.owner] = 0
                    corpse_count += 1
                del self.event_queue[index]
            index -= 1
        return corpse_count

    def game_over(self):
        """
        Check if the game is over
        :return: (bool)
        """
        num_glads = sum([1 for (t, g) in self.event_queue if g.type is "gladiator"])
        return bool(num_glads <= 1)
