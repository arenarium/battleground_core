
class GameEngine(object):
    """This is an interface for the game engine class.
    An the engine for a specific game
    should implement these functions.

    """

    def __init__(self, num_players, type, **kwargs):
        self.num_players = num_players
        self.current_player = 0
        self.type = type

    def get_game_name(self):
        """
        :returns: the type of the current game.

        """
        return self.type

    def get_state(self):
        """get the current state of the game to be passed to an agent
        :returns: the current game state.

        """
        raise NotImplementedError()

    def get_save_state(self):
        """
        :returns: the state of the game as it should be saved in the database

        """
        raise NotImplementedError()

    def get_current_player(self):
        """This will be used by the game runner to determine which player should
        make the next move

        :returns: index of players list of GameRunner

        """
        raise NotImplementedError()

    def reset(self):
        """Initialize the game to the starting point."""
        raise NotImplementedError()

    def move(self, move):
        """Do a move on behalf of the current player.
        This function is called by the game runner with a move for the
        current player.

        :param move: the move returned by the current player.

        """
        raise NotImplementedError()

    def game_over(self):
        """Check if the game is over.

        :returns: (bool) is the game over.

        """
        raise NotImplementedError()
