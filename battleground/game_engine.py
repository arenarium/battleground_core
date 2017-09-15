"""
This is an interface for the game engine class.On the engine for a specific game
Should implement these functions.
"""


class GameEngine(object):
    def __init__(self, num_players, type, **kwargs):
        self.num_players = num_players
        self.current_player = 0
        self.type = type

    def get_game_name(self):
        """
        return the name of this game (i.e. game type)
        """
        return self.type

    def get_state(self):
        raise NotImplementedError()

    def get_current_player(self):
        """
        This will be used by the game runner to determine which player should
        make the next move
        (only turn-based games!)
        :returns index of players list of GameRunner
        """
        raise NotImplementedError()

    def reset(self):
        """
        Initialize the game to the starting point
        """
        raise NotImplementedError()

    def move(self, move):
        """
        Do a move on behalf of the current player
        (only turn-based games!)
        """
        raise NotImplementedError()

    def game_over(self):
        """
        Check if the game is over
        """
        raise NotImplementedError()
