from battleground.game_engine import GameEngine

from games.arena.calc import calc
from games.arena.dungeon import Dungeon
from games.arena.event import Event
from games.arena.gladiator import Gladiator

import bisect
import random


class ArenaGameEngine(GameEngine):
    """
    An arena game engine based on an event queue.
    """

    def __init__(self, type, size, gladiator_stats={}):
        """
        :param type: str
        :param size: [int, int]
        :param gladiator_stats: list of dictionaries
                    each dict should have the form
                    { "pos": [int, int],
                      "name": (unique) str,
                      "team": int,
                      "stats": {"str": int, "dex": int, "con": int},
                      "skills": {"melee": int, "eva": int, "speed": int}
                    }

            initializing:
            self.current_player
            self.type
        """
        super().__init__(type)
        self.num_players = len(gladiator_stats)
        self.gladiators = [Gladiator(pos=g["pos"],
                                     name=g["name"],
                                     team=g["team"],
                                     stats=g["stats"],
                                     skills=g["skills"])
                           for g in gladiator_stats]
        self.dungeon = Dungeon(size=size)
        # initialize event queue by sorting gladiators by their speed
        # returns list of tuples
        self.event_queue = sorted([(g.get_speed() + calc.noise(), g) for g in self.gladiators],
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
        :returns index of players list of GameRunner
        """
        return self.gladiators.index(self.event_queue[0][1])

    def reset(self):
        """
        Initialize the game to the starting point
        """
        raise NotImplementedError()

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

        glad_event_time = time + glad.get_cost(name, value) + calc.noise()
        glad_event = Event(owner=glad,
                      time_stamp=glad_event_time,
                      type=name,
                      origin=glad.pos,
                      target=target,
                      value=value)

        bisect.insort(self.event_queue, (glad_event_time, glad_event))
        bisect.insort_right(self.event_queue, (glad_event_time, glad))

        if isinstance(self.event_queue[0][1], Event):
            (event_time, event) = self.event_queue.pop(0)

            while isinstance(event, Event):
                # handle events
                if event.name is "attack":
                    event.target.chp -= event.owner.attack(event.target)
                    if event.target.chp < 0:
                        index = self.event_queue.index((_, event.target))
                        del self.event_queue[index]
                elif event.name is "move":
                    event.owner.move(event.target)
                elif event.name is "boost":
                    event.owner.set_boosts(event.target, event.value)

                (event_time, event) = self.event_queue.pop(0)

        self.current_player = self.get_current_player()

        return None

    def game_over(self):
        """
        Check if the game is over
        """
        num_glads = sum([1 for g in self.event_queue if isinstance(g, Gladiator)])
        return bool(num_glads == 1)
