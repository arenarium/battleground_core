from battleground.agent import Agent
import random


class BasicAgent(Agent):
    def __init__(self):
        super().__init__()

    def move(self, options, state):
        return {"value": random.choice(options)}

    def observe(self, state):
        raise NotImplementedError()
