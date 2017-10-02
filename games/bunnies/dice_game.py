"""
game self.state is a set of player scores, plus a board self.state
board self.state is the set of dice self.states plus the current player
"""
import random
import copy
from battleground.game_engine import GameEngine

NUM_DICE = 7
END_SCORE = 333


class DiceGame(GameEngine):
    def __init__(self, num_players, type, state=None):
        """
        state should be a dict with the following elements:
        state = {
          "rollables": [1]*dice_game.NUM_DICE,
          "bunnies": [0]*dice_game.NUM_DICE,
          "hutches": [0]*dice_game.NUM_DICE,
          "movables": [1]*dice_game.NUM_DICE,
          "currentPlayer": 0,
          "scores": {0:0},
          "extraBunnies": 0,
          "message": "",
          "allowedMoves": {"roll":0,"stay":0,"reset":0,"moveBunny":1,"moveHutch":0},
          "boardValue": 0,
          "lastPlayer": self.num_players,
          "lastRound": False
        }
        """
        super().__init__(num_players, type)
        self.state = state
        if self.state is None:
            # if state is not provided, use default starting state
            self.reset()

    def get_game_name(self):
        """
        :returns (char) the name of this game (i.e. game type)
        """
        return "Bunnies"

    def get_state(self):
        """
        :returns self.state
        """
        return self.state

    @staticmethod
    def decode_state(state):
        return state

    @staticmethod
    def decode_move(move):
        return move

    def get_current_player(self):
        """
        :returns (int) current player ID
        """
        return self.state["currentPlayer"]

    def reset(self):
        """
        (re)set game into initial state
        :returns self.state
        """
        self.state = {}  # start with a fresh empty dict
        self.state["rollables"] = [random.randint(1, 6) for x in range(NUM_DICE)]
        for name in ["bunnies", "hutches"]:
            self.state[name] = [0] * NUM_DICE
        self.state["movables"] = [1] * NUM_DICE
        self.state["currentPlayer"] = 0
        # scores = {playerID, score}
        # The scores dictionary is dynamically generated.
        # For each player not in the dict, _do_stay() adds an entry.
        self.state["scores"] = {i: 0 for i in range(self.num_players)}
        self.state["extraBunnies"] = 0
        self.state["message"] = ""
        # if no bunnies were rolled
        if self._youre_dead():
            self.state["allowedMoves"] = {"roll": 0, "stay": 1, "reset": 0, "moveBunny": 0, "moveHutch": 0}
        else:  # at least one bunny needs to be moved before being able to roll again or stay with the result
            self.state["allowedMoves"] = {"roll": 0, "stay": 0, "reset": 0, "moveBunny": 1, "moveHutch": 0}
        self.state["boardValue"] = 0
        self.state["lastPlayer"] = -1
        self.state["lastRound"] = False
        return self.state

    def _get_num_bunnies(self):
        """
        Two 1's count as 10 bunnies.
        :returns (int) number of bunnies in the bunnies bin
        """
        ones = self.state["bunnies"].count(1)
        twos = self.state["bunnies"].count(2)
        return (ones // 2) * 10 + twos * 2 + ones % 2 + self.state["extraBunnies"]

    def _score(self):
        """
        score = bunnies * hutches
        :returns (int) current board value of current player
        """
        num_bunnies = self._get_num_bunnies()
        num_hutches = max(self.state["hutches"])
        num_hutches = max(num_hutches, 1)
        return num_hutches * num_bunnies

    @staticmethod
    def _check_bunnies(bunnies):
        """
        :returns (bool) if list of bunnies is valid, (char) error message if not
        """
        if not all([x <= 2 for x in bunnies]):
            return False, "Only bunnies are allowed in bunnies container!"
        return True, ""

    @staticmethod
    def _check_hutches(hutches):
        """
        :returns (bool) if list of hutches is valid, (char) error message if not
        """
        if not all([x != 1 for x in hutches]):
            return False, "No bunnies allowed in hutch container!"
        if 2 < min(x for x in hutches if x > 0):
            return False, "Hutches must start from 2."
        old_x = max(hutches) + 1
        for x in sorted(hutches, reverse=True):
            if x == 0:
                break
            if x == old_x - 1:
                old_x = x
            else:
                return False, "Hutches must be consecutive and unique."
        return True, ""

    def _is_valid(self, move):
        """
        :returns (bool) if a move is valid given current state
        """
        assert "name" in move
        assert "value" in move

        move_name = move["name"]
        dice_ID = move["value"]

        state_copy = copy.deepcopy(self.state)
        # if move is allowed
        if self.state["allowedMoves"][move_name] == 1:
            if move_name == "moveBunny":
                self._do_move_bunny(state_copy, dice_ID)
                # if hutches in bunnies container
                valid, message = self._check_bunnies(state_copy["bunnies"])
                if not valid:
                    self.state["message"] = message
                    return False
            elif move_name == "moveHutch":
                self._do_move_hutch(state_copy, dice_ID)
                # check if no bunnies in hutches container and if hutches are ok
                valid, message = self._check_hutches(state_copy["hutches"])
                if not valid:
                    self.state["message"] = message
                    return False
            self.state["message"] = ""
            return True
        else:
            return False

    def _youre_dead(self):
        """
        :returns (bool) if you're dead because you rolled no bunnies
        """
        return all([x > 2 or x == 0 for x in self.state["rollables"]])

    def _do_roll(self):
        """
        roll mechanics
        :returns self.state
        """
        # if no rollable dice
        if all([x == 0 for x in self.state["rollables"]]):
            # record existing bunnies
            self.state["extraBunnies"] = self._get_num_bunnies()
            # recycle dice from bunnies for new rollable dice
            self.state["rollables"] = [1 if x > 0 else 0 for x in self.state["bunnies"]]
            # reset bunnies
            self.state["bunnies"] = [0] * 7

        # update movable dice
        self.state["movables"] = [1 if x > 0 else 0 for x in self.state["rollables"]]

        # and do the roll
        self.state["rollables"] = [random.randint(1, 6) if x > 0 else 0 for x in self.state["rollables"]]

        # check if roll ends turn
        if self._youre_dead():
            self.state["message"] = "You rolled no bunnies, your turn is over."
            # dead player manually ends turn, no automatic switch to new player
            self.state["allowedMoves"] = {"roll": 0, "stay": 1, "reset": 0, "moveBunny": 0, "moveHutch": 0}
            self.state["boardValue"] = 0
        else:  # if roll did not end turn, update allowed moves and board value
            self.state["allowedMoves"] = {"roll": 0, "stay": 0, "reset": 0, "moveBunny": 1, "moveHutch": 0}
            self.state["boardValue"] = self._score()
        return self.state

    def _do_stay(self):
        """
        ends current player's turn and moves on to next player
        :returns self.state
        """
        player_index = self.get_current_player()

        # if not able to roll again
        if self.state["allowedMoves"]["roll"] == 0:
            # move to next player and reset dice
            self.state["currentPlayer"] = (player_index + 1) % self.num_players
            return self._do_reset()
        else:  # if able to roll again
            # update movable dice
            self.state["movables"] = [1 if x > 0 else 0 for x in self.state["rollables"]]
            # note board value
            board_value = self._score()
            # if the current player has an initialized score
            if player_index in self.state["scores"]:
                self.state["scores"][player_index] += board_value
            else:  # if not, a new score is initialized
                self.state["scores"][player_index] = board_value
            # move to next player, note score and reset allowed moves
            self.state["currentPlayer"] = (player_index + 1) % self.num_players
            self.state["boardValue"] = self._score()
            self.state["allowedMoves"] = {"roll": 1, "stay": 0, "reset": 1, "moveBunny": 0, "moveHutch": 0}
            return self.state

    def _do_reset(self):
        """
        resets state into initial state, leaving current player and scores the same
        :returns self.state
        """
        self.state["rollables"] = [random.randint(1, 6) for x in self.state["rollables"]]
        for name in ["bunnies", "hutches"]:
            self.state[name] = [0] * 7
        self.state["movables"] = [1] * 7
        self.state["extraBunnies"] = 0
        self.state["message"] = ""
        # at least one bunny needs to be moved before being able to roll again or pass on
        self.state["allowedMoves"] = {"roll": 0, "stay": 0, "reset": 0, "moveBunny": 1, "moveHutch": 0}
        self.state["boardValue"] = self._score()

        if self._youre_dead():
            self.state["message"] = "You rolled no bunnies, your turn is over."
            # dead player manually ends turn, no automatic switch to new player
            self.state["allowedMoves"] = {"roll": 0, "stay": 1, "reset": 0, "moveBunny": 0, "moveHutch": 0}
            self.state["boardValue"] = 0

        return self.state

    @staticmethod
    def _do_move_bunny(state, dice_ID):
        """
        moves the die at position dice_ID from rollables to bunnies
        at least one bunny needs to be moved before being able to roll again or pass on
        :returns self.state
        """
        state["bunnies"][dice_ID] = state["rollables"][dice_ID]
        state["rollables"][dice_ID] = 0
        state["movables"][dice_ID] = 0
        state["allowedMoves"]["roll"] = 1
        state["allowedMoves"]["stay"] = 1
        state["allowedMoves"]["moveHutch"] = 1
        # if no bunny to take
        if state["rollables"].count(0) == NUM_DICE:
            state["allowedMoves"]["moveHutch"] = 0
            state["allowedMoves"]["moveBunny"] = 0
        elif 1 not in state["rollables"] and 2 not in state["rollables"]:
            state["allowedMoves"]["moveBunny"] = 0
        return state

    @staticmethod
    def _do_move_hutch(state, dice_ID):
        """
        moves the die at position dice_ID from rollables to hutches
        :returns self.state
        """
        state["hutches"][dice_ID] = state["rollables"][dice_ID]
        state["rollables"][dice_ID] = 0
        state["movables"][dice_ID] = 0
        # if no next hutch to take
        max_hutch = max(state["hutches"])
        if state["rollables"].count(0) == NUM_DICE:
            state["allowedMoves"]["moveBunny"] = 0
            state["allowedMoves"]["moveHutch"] = 0
        elif (max_hutch + 1) not in state["rollables"]:
            state["allowedMoves"]["moveHutch"] = 0
        return state

    def move(self, move):
        """
        checks if (dict) move is valid given current state and applies move
        :returns self.state
        """
        assert "name" in move
        assert "value" in move

        move_name = move["name"]
        dice_ID = move["value"]

        if self._is_valid(move):
            self.state["message"] = ""
            if move_name == "roll":
                self._do_roll()
            elif move_name == "stay":
                self._do_stay()
            elif move_name == "reset":
                self._do_reset()
            elif move_name == "moveBunny":
                self._do_move_bunny(self.state, dice_ID)
            elif move_name == "moveHutch":
                self._do_move_hutch(self.state, dice_ID)
        else:
            self.state["message"] = "This is not a valid move."

        if self._last_round():
            if not self.state["lastRound"]:
                self.state["lastRound"] = True
                self.state["lastPlayer"] = (self.state["currentPlayer"] - 2) % self.num_players

        # No moves are allowed any longer if the game is over.
        if self.game_over():
            self.state["allowedMoves"] = {"roll": 0, "stay": 0, "reset": 0, "moveBunny": 0, "moveHutch": 0}
            self.state["message"] = str(self.state["scores"])

        return self.state

    def _last_round(self):
        return END_SCORE <= max(self.state["scores"].values())

    def game_over(self):
        """
        :returns (bool) if the game is over
        """
        return bool(self.state["currentPlayer"] == self.state["lastPlayer"])
