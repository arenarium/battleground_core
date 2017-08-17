import agent
import dice_game

class SimpleAgent(agent.Agent):

    def __init__(self,threshold=20):
        self.threshold=threshold

    def move_bunnies(self,state):
        return state

    def move_hutches(self,state):
        return state

    def do_move(self,state):
        my_game = dice_game.DiceGame(state)
        board_value = my_game.score()
        if board_value>20:
            move = "stay"
        return move, state
