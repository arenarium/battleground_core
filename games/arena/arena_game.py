from battleground.game_engine import GameEngine

from games.arena.dungeon import Dungeon
from games.arena.gladiator import Gladiator

from collections import deque
import random


class ArenaGameEngine(GameEngine):

    def __init__(self, num_players, type, size):
        super().__init__(num_players, type)
        self.num_players = num_players
        self.type = type
        self.dungeon = self.load_dungeon(size)
        self.event_queue = deque([])

    def load_dungeon(self, size):
        dungeon = Dungeon(size=size)
        return dungeon

    def get_game_name(self):
        return self.type

    def get_state(self):
        raise NotImplementedError()

    def get_current_player(self):
        raise NotImplementedError()

    def reset(self):
        raise NotImplementedError()

    def move(self, move):
        raise NotImplementedError()

    def game_over(self):
        raise NotImplementedError()
