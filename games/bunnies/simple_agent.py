from battleground import agent
import random
# if __name__ == "__main__":
#     import dice_game
# else:
#     from . import dice_game


class SimpleAgent(agent.Agent):
    def __init__(self, threshold=20):
        super().__init__()
        self.threshold = threshold

    def move(self, options, state):
        # my_game = dice_game.DiceGame(num_players=len(state["scores"]), type="Bunnies", state=state)
        #
        # available_move_names = {k for k, v in my_game.state["allowedMoves"].items() if v == 1}
        # # caught these two cases in _do_move_bunny or _do_move_hutch functions
        # if ("moveBunny" in available_move_names
        #         and 1 not in my_game.state["rollables"]
        #         and 2 not in my_game.state["rollables"]):
        #     available_move_names.remove("moveBunny")
        #
        # max_hutch = max(1, max(my_game.state["hutches"]))
        # if ("moveHutch" in available_move_names
        #         and (max_hutch + 1) not in my_game.state["rollables"]):
        #     available_move_names.remove("moveHutch")
        #
        # chosen_move_name = random.choice(list(available_move_names))
        #
        # if chosen_move_name == "moveBunny":
        #     # prefer taking a 1 instead of a 2 as bunny
        #     if 1 in my_game.state["rollables"]:
        #         chosen_move_value = my_game.state["rollables"].index(1)
        #     elif 2 in my_game.state["rollables"]:
        #         chosen_move_value = my_game.state["rollables"].index(2)
        #     else:  # not happening because we checked before that 1 or 2 are in the list
        #         chosen_move_value = 0
        # elif chosen_move_name == "moveHutch":
        #     # max_hutch + 1 is definitely in rollables as checked above
        #     chosen_move_value = my_game.state["rollables"].index(max_hutch + 1)
        # else:  # otherwise doesn't matter
        #     chosen_move_value = 0

        name, values = random.choice(list(options.items()))
        value = random.choice(values)

        move = {"name": name,
                "value": value}

        return move

    def observe(self, state):
        raise NotImplementedError()