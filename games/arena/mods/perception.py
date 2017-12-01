import random

from games.arena import arena_game
from games.arena import dungeon
from games.arena import event
from games.arena import gladiator


class ArenaGameEngine(arena_game.ArenaGameEngine):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_state(self, observer):
        return {"gladiators": [g.get_init(observer) for g in self.gladiators],
                "dungeon": self.dungeon.get_init(observer),
                "queue": [(t, e.get_init(observer)) for t, e in self.event_queue],
                "scores": self.scores
                }


class Dungeon(dungeon.Dungeon):
    def get_init(self, observer):
        init = super().get_init()
        init = observer.observe(init)
        return init


class Event(event.Event):
    def get_init(self, observer):
        init = super().get_init()
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

    def get_init(self, observer):
        init = super().get_init()
        init["perception"] = self.perception
        init = observer.observe(init)
        return init

    def reset(self):
        super().reset()
        self.perception = 0
        if hasattr(self, "boosts"):
            self.boosts["perception"] = 0
        return None

    def get_perception(self):
        boost = 0
        if hasattr(self, "boosts"):
            boost = self.boosts["perception"]
        perc = self.perception + boost
        return perc

    def get_perception_p(self):
        perc = self.get_perception()
        if perc < 0:
            p = 1 / (2 - perc)
        else:
            p = 1 - 1 / (2 + perc)
        return p

    def observe(self, init_state):
        """
        There is the chance to observe the value to a key of an init_state entry with
        probability get_perception_p.
        :param init_state: dict
        :return: observed init_state
        """
        for key, _ in init_state:
            if self.get_perception_p() < random.uniform(0,1):
                init_state[key] = None
        return init_state
