from . import agent


class FallbackAgent(agent.Agent):

    def move(self, state):
        return {}
