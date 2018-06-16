from battleground.agent import Agent
from battleground.games.arena import building_blocks


class ArenaAgent(Agent):

    def move(self, state):
        """
        Can only play arena games with position mod.
        :param state: state of the game
        :return: dict of chosen move
        """

        return building_blocks.random_walk(state)
