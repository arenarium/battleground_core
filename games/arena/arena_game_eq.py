
from games.arena.arena import ArenaGameEngine
from games.arena.dungeon import Dungeon
from games.arena.gladiator import Gladiator

from collections import deque
import random


class EQArenaGameEngine(ArenaGameEngine):
    """
    EQ = Event Queue
    One event happens at a time step.
    """

    def __init__(self, type, size, gladiator_stats={}):
        super().__init__(type, size, gladiator_stats)
        self.event_queue = deque([])
        # sort gladiators by their speed
        # sorted(glads, key=lambda glad: glad.get_speed())
        self.state = {"gladiators": self.gladiators,
                      "dungeon": self.dungeon,
                      "queue": self.event_queue}

    def get_state(self):
        return self.state

    def get_current_player(self):
        raise NotImplementedError()

    def reset(self):
        raise NotImplementedError()

    def move(self, move):
        raise NotImplementedError()

    def game_over(self):
        raise NotImplementedError()
