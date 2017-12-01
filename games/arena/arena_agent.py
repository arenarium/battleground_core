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

    def move(self, state):
        # my_game = arena_game.ArenaGameEngine(num_players=len(state["gladiators"]),
        #                                      type="test_arena",
        #                                      state=state)
        # my_gladiator = state["queue"][0][1]["owner"]
        # options = my_game.get_move_options(my_gladiator)

        options = state["move_options"]

        option = random.choice(options)
        name = option["name"]
        target_dict = random.choice(option["targets"])
        target = target_dict["target"]
        value = random.choice(target_dict["values"])

        move = {"name": name,
                "target": target,
                "value": value}
        return move

    def observe(self, state):
        raise NotImplementedError()
