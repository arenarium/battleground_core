from battleground.agent import Agent
import random


class BasicAgent(Agent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def move(self, state):
        return {"value": random.randint(5, 20)}
