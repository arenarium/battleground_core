from battleground.agent import Agent
import random


class ArenaAgent(Agent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def move(self, state):
        """
        This method is written such that this agent can also play the bunnies
        game and the basic games.
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
