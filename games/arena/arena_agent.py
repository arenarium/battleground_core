from battleground.agent import Agent
from games.arena.arena_game import ArenaGameEngine

import random


class ArenaAgent(Agent):

    def move(self, state):
        # glad_stats = [g.get_init() for g in state["gladiators"]]
        my_game = ArenaGameEngine(num_players=len(state["gladiators"]),
                                             type="Arena",
                                             state=state)
        my_gladiator = state["queue"][0]
        names = my_game.get_move_names(my_gladiator)
        targets = my_game.get_targets(my_gladiator)
        values = my_game.get_values(my_gladiator)
        name = random.choice(names)
        target = random.choice(targets[name])
        value = random.choice(values[name])
        move = {"name": name,
                "target": target,
                "value": value}
        return move

    def observe(self, state):
        raise NotImplementedError()
