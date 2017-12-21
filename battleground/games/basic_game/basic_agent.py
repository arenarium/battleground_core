from battleground.agent import Agent
import random


class BasicAgent(Agent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def move(self, state):
        move = {}

        if state is not None:
            if "move_options" in state:
                options = state["move_options"]
                if "values" in options:
                    value = random.choice(options["values"])
            else:
                # default value
                value = random.randint(5, 20)
                print("Agent is taking default values.")

        try:
            move["value"] = value
        except NameError:
            pass

        return move
