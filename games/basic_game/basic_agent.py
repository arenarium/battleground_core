from battleground.agent import Agent
import random


class BasicAgent(Agent):
    def __init__(self):
        super().__init__()

    def move(self, state):
        return {"value": random.randint(5, 20)}

    def observe(self, state):
        raise NotImplementedError()
