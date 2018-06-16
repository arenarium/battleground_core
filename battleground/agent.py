
class Agent(object):
    """This is an interface for the agent class.
    Every agent should sub-class this class.
    The entrypoint for this class is the move() function.
    """

    def __init__(self, **kwargs):
        self.set_memory(None)

    def move(self, state):
        """Main entrypoint for the agent class, agent logic goes here.
        This function is called by the game runner when it is this
        agent's turn to make a move.

        :param state: The current game state.

        :returns: A valid move.

        """
        raise NotImplementedError()

    def observe(self, state):
        """
        This function is called by the game engine every time an update to
        the game state is available. (Even on other player's turns.)

        :param state: The current game state.

        """
        pass

    def get_memory(self, default=None):
        """
        This function can be used by an agent to get it's persistent memory.
        This function is also used by site runner to get the agent's memory
        at the end of a game and store it in the database.

        :param default:  (Default value = None) If agent memory is not set,
            return the default value.

        :returns: the persistent memory of the agent.

        """
        return default if self._data is None else self._data

    def set_memory(self, data):
        """Set the persistent memory of the agent.
        This function should be called by the agent if the persistent memory
        needs to be updated.
        This function is also called by the site runner at the start of a game.

        :param data: The data to save.

        """
        self._data = data
