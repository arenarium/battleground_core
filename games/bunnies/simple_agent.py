from battleground import agent
import random


class SimpleAgent(agent.Agent):
    def __init__(self, threshold=20):
        super().__init__()
        self.threshold = threshold

    def move(self, state):
        options = state["move_options"]
        name, values = random.choice(list(options.items()))
        value = random.choice(values)
        move = {"name": name,
                "value": value}
        return move

    def observe(self, state):
        raise NotImplementedError()
