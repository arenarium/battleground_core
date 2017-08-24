import agent
import dice_game
import random


class SimpleAgent(agent.Agent):
    def __init__(self, threshold=20):
        self.threshold = threshold

    def move(self, state):
        my_game = dice_game.DiceGame(state)
        available_move_names = {k for k, v in my_game.state["allowedMoves"].items() if v == 1}
        chosen_move_name = random.choice(list(available_move_names))
        # todo: don't try to put bunnies into hutches and vice versa
        if chosen_move_name == "moveBunny":
            chosen_move_value = random.randint(0, dice_game.NUM_DICE - 1)
        elif chosen_move_name == "moveHutch":
            chosen_move_value = random.randint(0, dice_game.NUM_DICE - 1)
        else:  # otherwise doesn't matter
            chosen_move_value = 0

        return [chosen_move_name, chosen_move_value]
