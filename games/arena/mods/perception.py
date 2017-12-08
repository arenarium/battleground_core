import random

from games.arena import arena_game
from games.arena import dungeon
from games.arena import event
from games.arena import gladiator


class ArenaGameEngine(arena_game.ArenaGameEngine):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_state(self, observer="player"):
        if observer is "player":
            observer = self.gladiators[self.get_current_player()]
        state = {"gladiators": [g.get_init(observer) for g in self.gladiators],
                 "dungeon": self.dungeon.get_init(observer),
                 "queue": [(t, e.get_init(observer)) for t, e in self.event_queue],
                 "scores": self.scores,
                 "move_options": self.get_move_options(self.get_current_player())
                 }
        return state

    def get_save_state(self):
        return self.get_state(observer=None)


class Dungeon(dungeon.Dungeon):
    def get_init(self, observer=None):
        init = super().get_init()
        if observer is not None:
            init = observer.observe(init)
        return init


class Event(event.Event):
    def get_init(self, observer=None):
        init = super().get_init()
        if observer is not None:
            init = observer.observe(init)
        return init


class Gladiator(gladiator.Gladiator):
    def __init__(self, perception=0, *args, **kwargs):
        """
        :param perception: ability to detect events
        """
        super().__init__(*args, **kwargs)

        self.perception = perception
        if hasattr(self, "boosts"):
            self.boosts["perception"] = 0
        # setting boosts["perception"] through boosts input is done in boosts mod

    def get_init(self, observer=None):
        init = super().get_init()
        init["perception"] = self.perception
        if observer is not None:
            init = observer.observe(init)
        return init

    def reset(self):
        super().reset()
        self.perception = 0
        if hasattr(self, "boosts"):
            self.boosts["perception"] = 0
        return None

    def get_perception(self):
        """
        Get current perception value
        :return: (int) perception
        """
        boost = 0
        if hasattr(self, "boosts"):
            boost = self.boosts["perception"]
        perc = self.perception + boost
        return perc

    def get_perception_p(self):
        """
        Get probability to observe something depending on current perception value
        perception:   -3,  -2,  -1,  0 ,   1,   2,   3
        probability: 1/5, 1/4, 1/3, 1/2, 2/3, 3/4, 4/5
        :return: (float) probability
        """
        perception = self.get_perception()
        if perception < 0:
            probability = 1 / (2 - perception)
        else:
            probability = 1 - 1 / (2 + perception)
        return probability

    def observe(self, init_state):
        """
        There is the chance to observe the value to a key of an init_state entry with
        probability get_perception_p.
        :param init_state: dict
        :return: observed init_state
        """
        for key, _ in init_state:
            if self.get_perception_p() < random.uniform(0, 1):
                init_state[key] = "?"
        return init_state
