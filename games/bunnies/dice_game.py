"""
game self.state is a set of player scores, plus a board self.state
board self.state is the set of dice self.states plus the current player
"""
import random
from battleground.game_engine import GameEngine

NUM_DICE = 7

class DiceGame(GameEngine):

    def __init__(self,state=None):

        self.state=state
        self.num_players = 2

    def set_state(self,state):
        """
        set the game state
        """
        self.state = state

    def _get_num_bunnies(self):
        """
        number bunnies in the bunnies bin. used for scoring.
        """
        ones = sum([int(int(x)==1) for x in self.state["bunnies"]])
        twos = sum([int(int(x)==2) for x in self.state["bunnies"]])
        return  (ones//2)*10+twos*2+ones%2 + self.state["extraBunnies"]

    def score(self):
        """
        return current board value
        """
        num_bunnies = self._get_num_bunnies()
        num_huches = max(self.state["hutches"])
        num_huches = max(num_huches,1)
        return num_huches*num_bunnies

    def check_hutches(self,hutches):
        if not all([x!=1 for x in hutches]):
            return False, "no bunnies allowed in hutch container"
        old_x = max(hutches)+1
        for x in sorted(hutches,reverse=True):
            if x==0:
                break
            if x==old_x-1:
                old_x =x
            else:
                return False, "hutches must be consecutive and unique"
        return True,""


    def is_valid(self,move):
        """
        check if a move is valid given current state
        """
        if self.state["allowedMoves"][move]==1:
            if not all([x<=2 for x in self.state["bunnies"]]):
                self.state["message"]="only bunnies allowed in bunnies container"
                return False
            valid, message = self.check_hutches(self.state["hutches"])
            if not valid:
                self.state["message"] = message
                return False
            return True
        else:
            return False

    def youre_dead(self):
        """
        you're dead if you rolled 0 bunnies
        """
        return all([int(x)>2 or int(x)==0 for x in self.state["rollable"]])

    def doroll(self):
        """
        roll mechanicts
        """
        if all([int(x)==0 for x in self.state["rollable"]]): # if no rollable dice
            self.state["extraBunnies"] = self._get_num_bunnies() # record existing bunnies
            self.state["rollable"] = [1 if int(x)>0 else 0 for x in self.state["bunnies"]] # recycle dice
            self.state["bunnies"] = [0]*7

        self.state["movable"] = [1 if int(x)>0 else 0 for x in self.state["rollable"]] # upate movable


        """ and do the roll """
        self.state["rollable"] = [random.randint(1,6) if int(x)>0 else 0 for x in self.state["rollable"]]

        if self.youre_dead(): # check if result ends turn
            self.state["message"]="No Bunnies, your turn is over."
            self.state["allowedMoves"] = {"roll":0,"stay":1,"reset":0}
            self.state["boardValue"] = 0
        else: # update allowed moves
            self.state["allowedMoves"] = {"roll":1,"stay":1,"reset":0}
            self.state["boardValue"] = self.score()
        return self.state

    def dostay(self):
        player_index = str(self.state["currentPlayer"])
        if self.state["allowedMoves"]["roll"]==0:
            self.state["currentPlayer"] = (int(player_index)+1)%self.num_players
            self.state["allowedMoves"] = {"roll":1,"stay":0,"reset":0}
            return self.reset()
        else:
            board_value = self.score()
            self.state["movable"] = [1 if int(x)>0 else 0 for x in self.state["rollable"]]
            if player_index in self.state["scores"]:
                self.state["scores"][player_index]=int(self.state["scores"][player_index])+board_value
            else:
                self.state["scores"][player_index]=board_value
            self.state["currentPlayer"] = (int(player_index)+1)%self.num_players
            self.state["boardValue"] = self.score()
            self.state["allowedMoves"] = {"roll":1,"stay":0,"reset":1}
            return self.state


    def reset(self):
        self.state['message']=""
        self.state["movable"] = [1]*7
        for name in ["hutches","bunnies"]:
            self.state[name] = [0]*7
        self.state["rollable"] = [random.randint(1,6) for x in self.state["rollable"]]
        self.state["boardValue"] = self.score()
        self.state["extraBunnies"] = 0
        self.state["allowedMoves"] = {"roll":1,"stay":0,"reset":0}
        return self.state


    def move(self,move):
        if self.is_valid(move):
            if move =="stay":
                self.dostay()
            elif move =="roll":
                self.doroll()
            elif move=="reset":
                self.reset()
        return self.state

    def get_current_player(self):
        return self.state["currentPlayer"]
