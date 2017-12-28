from battleground.agent import Agent
import random


class ArenaAgent(Agent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def move(self, state):
        """
        This method is written such that this agent can also play the bunnies game and the basic games.
        :param state: state of the game
        :return: dict of chosen move
        """
        move = {}

        if state is not None:
            if "move_options" in state:
                options = state["move_options"]
                if isinstance(options, list):
                    options = random.choice(options)
                if "name" in options:
                    move["name"] = options["name"]

                if "tools" in options:
                    options = random.choice(options["tools"])
                if "tool" in options:
                    move["tool"] = options["tool"]

                if "targets" in options:
                    options = random.choice(options["targets"])
                if "target" in options:
                    move["target"] = options["target"]

                if "values" in options:
                    move["value"] = random.choice(options["values"])
            else:
                # default values
                move["name"] = "stay"
                move["tool"] = None
                move["target"] = None
                move["value"] = 1
                print("Agent is taking default values.")

        return move
