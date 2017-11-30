from battleground import agent
# from games.arena.arena_game import ArenaGameEngine
# if __name__ == "__main__":
#     import arena_game
# else:
#     from . import arena_game

import random


class ArenaAgent(agent.Agent):
    def __init__(self):
        super().__init__()

    def move(self, options, state):
        # my_game = arena_game.ArenaGameEngine(num_players=len(state["gladiators"]),
        #                                      type="test_arena",
        #                                      state=state)
        # my_gladiator = state["queue"][0][1]["owner"]
        # options = my_game.get_move_options(my_gladiator)

        if "attack" in options.keys():
            name = "attack"
            targets = options["attack"]
        else:
            name, targets = random.choice(list(options.items()))
        target, values = random.choice(list(targets.items()))
        value = random.choice(values)

        move = {"name": name,
                "target": target,
                "value": value}
        return move

    def observe(self, state):
        raise NotImplementedError()
