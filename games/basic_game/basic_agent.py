from battleground.agent import Agent
import random

class BasicAgent(Agent):

    def move(self,state):
        return {"value":random.randint(5,20)}
