from battleground.game_engine import GameEngine
import random

class BasicGameEngine(GameEngine):

    def __init__(self, num_players):
        super().__init__(num_players)
        self.reset()


    def reset(self):
        """
        Initialize the game to the starting point
        """
        self.last_round = False
        self.last_player = None
        self.scores = [0]*self.num_players
        self.current_player=0
        self.turn=0

    def get_state(self):
        return {"scores":self.scores, "turn":self.turn}

    def move(self,move):
        """
        Do you move on behalf of the current player
        """
        assert "value" in move

        value = move["value"]
        roll = random.randint(1,25)

        if value<roll:
            self.scores[self.current_player]+=value
            if not self.last_round and self.scores[self.current_player]>=100:
                self.last_round=True
                self.last_player = self.current_player
        else:
            self.current_player = (self.current_player+1)%self.num_players

        self.turn+=1


    def game_over(self):
        """
        Check if the game is over
        """
        if self.last_round and self.last_player == self.current_player:
            return True
        else:
            return False

    def get_current_player(self):
        """
        This will be used by the game runner to determine which player should
        make the next move
        """
        return self.current_player
