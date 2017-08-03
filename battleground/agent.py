
class Agent(object):

    def __init__(self):
        pass

    def move(self,state):
        raise NotImplementedError()

    def observe(self,state):
        raise NotImplementedError()
