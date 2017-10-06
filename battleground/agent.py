
class Agent(object):

    def __init__(self, data=None, **kwargs):
        pass

    def move(self, state):
        raise NotImplementedError()

    def observe(self, state):
        raise NotImplementedError()

    def get_data_to_save():
        """
        the value returned here will be passed as the "data" parameter on the
        next initialization of the agent.
        """
        return None
