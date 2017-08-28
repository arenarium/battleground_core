from battleground.agent import Agent


class ArenaAgent(Agent):

    def move(self, state):
        raise NotImplementedError()

    def observe(self,state):
        raise NotImplementedError()
