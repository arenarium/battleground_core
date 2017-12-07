
class Agent(object):

    def __init__(self, **kwargs):
        self.set_memory(None)

    def move(self, state):
        raise NotImplementedError()

    def observe(self, state):
        pass

    def get_memory(self, default=None):
        """
        the value returned here will be passed as the "data" parameter
        in set_data_to_save on the
        next initialization of the agent.
        """
        return default if self._data is None else self._data

    def set_memory(self, data):
        """
        the value set here is read from the database on init
        """
        self._data = data
