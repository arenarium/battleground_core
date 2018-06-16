from battleground.agent import Agent
from battleground.games.arena import building_blocks


class ArenaAgent(Agent):

    def move(self, state):
        """
        Attack nearest other or move towards nearest other.
        """

        # try attack move is valid
        move = building_blocks.attack_closest(state)
        if move is not None:
            return move

        # if attack is not possible, move towards closest other
        closest = building_blocks.closest_other_location(state)
        move = building_blocks.move_toward(state, closest)
        if move is not None:
            return move

        # if move is not possible, do nothing.
        return {}
