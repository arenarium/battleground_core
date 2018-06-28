
class GameEngine(object):
    """
    This is an interface for the game engine class.
    An engine for a specific game
    should implement these functions.

    """

    def __init__(self, num_players, type, **kwargs):
        self.num_players = num_players
        self.current_player = 0
        self.type = type

    def get_game_name(self):
        """
        :returns: (str) the type of the current game.

        """
        return self.type

    def get_state(self):
        """
        Get the current state of the game.

        :returns: the current game state.

        """
        raise NotImplementedError()

    def get_save_state(self):
        """
        :returns: the state of the game as it should be saved in the database.

        """
        raise NotImplementedError()

    def get_current_player(self):
        """
        This is used by the game runner to determine which player should
        make the next move

        :returns: (int) index of the current player in the players list of the GameRunner

        """
        raise NotImplementedError()

    def reset(self):
        """
        Initialize the game to the starting point.
        """
        raise NotImplementedError()

    def move(self, move):
        """
        Resolve a move in the game engine on behalf of the current player.
        This function is called by the game runner, taking the agent's chosen move of the
        current player.

        :param move: the move returned by the agent of the current player.

        """
        raise NotImplementedError()

    def game_over(self):
        """Check if the game is over.

        :returns: (bool) is the game over.

        """
        raise NotImplementedError()
