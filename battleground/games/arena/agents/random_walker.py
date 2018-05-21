from battleground.agent import Agent
import random


class ArenaAgent(Agent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def move(self, state):
        """
        Can only play arena games with position mod.
        :param state: state of the game
        :return: dict of chosen move
        """
        my_move = {}

        if state is not None:
            if "move_options" in state:
                for move in state['move_options']:
                    if move['type'] == 'move':  # walk around
                        my_move["type"] = "move"
                        my_move["tool"] = None
                        my_move["target"] = random.choice(move['targets'])
                        my_move["value"] = 1

        return my_move
