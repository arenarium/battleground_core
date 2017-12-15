from battleground import agent
import random


class SimpleAgent(agent.Agent):
    def __init__(self, threshold=20, **kwargs):
        super().__init__(**kwargs)
        self.threshold = threshold

    def move(self, state):
        options = state["move_options"]
        name, values = random.choice(list(options.items()))
        value = random.choice(values)
        move = {"name": name,
                "value": value}
        return move
