from battleground.agent import Agent
from battleground.games.arena import building_blocks


class ArenaAgent(Agent):

    def move(self, state):
        """
        Can only play arena games with position mod.
        :param state: state of the game
        :return: dict of chosen move
        """

        # try if attack move is valid
        move = building_blocks.attack_closest(state)
        if move is not None:
            return move

        # if no attack possible:
        return building_blocks.random_move(state, seppuku=False)
