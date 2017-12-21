from battleground.agent import Agent
import random


class SimpleAgent(Agent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def move(self, state):
        """
        This method is written such that this agent can also play basic games.
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
                    name = options["name"]
                if "values" in options:
                    value = random.choice(options["values"])
            else:
                # default values
                name = "stay"
                value = None
                print("Agent is taking default values.")

        try:
            move["name"] = name
        except NameError:
            pass
        try:
            move["value"] = value
        except NameError:
            pass

        return move
