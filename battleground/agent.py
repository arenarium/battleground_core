
class Agent(object):

    def __init__(self, **kwargs):
        pass

    def move(self, options, state):
        raise NotImplementedError()

    def observe(self, state):
        raise NotImplementedError()
