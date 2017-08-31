from battleground.game_engine import GameEngine

from games.arena.dungeon import Dungeon
from games.arena.gladiator import Gladiator

from collections import deque
import random


class ArenaGameEngine(GameEngine):
    """
    An arena (super) class defining everything except the gameplay rules.
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
        # names have to be unique
        self.gladiators = {g["name"]: Gladiator(pos=g["pos"],
                                                name=g["name"],
                                                team=g["team"],
                                                stats=g["stats"],
                                                skills=g["skills"])
                           for g in gladiator_stats}
        self.dungeon = Dungeon(size=size)

    def get_game_name(self):
        return self.type

    def get_state(self):
        raise NotImplementedError()

    def get_current_player(self):
        """
        This will be used by the game runner to determine which player should
        make the next move
        :returns index of players list
        """
        raise NotImplementedError()

    def reset(self):
        raise NotImplementedError()

    def move(self, move):
        raise NotImplementedError()

    def game_over(self):
        raise NotImplementedError()
