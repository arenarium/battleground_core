"""
This is an interface for the game engine class.On the engine for a specific game
Should implement these functions.
"""

class GameEngine(object):

    def __init__(self,num_players):
        self.num_players = num_players
        self.scores = [0]*num_players
        self.current_player = 0

    def reset(self):
        """
        Initialize the game to the starting point
        """
        raise NotImplementedError()

    def move(self,move):
        """
        Do you move on behalf of the current player
        """
        raise NotImplementedError()

    def game_over(self):
        """
        Check if the game is over
        """
        raise NotImplementedError()

    def get_current_player(self):
        """
        This will be used by the game runner to determine which player should
        make the next move
        """
        raise NotImplementedError()

    def get_state(self):
        raise NotImplementedError()
