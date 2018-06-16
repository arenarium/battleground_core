from battleground.agent import Agent


class ArenaAgent(Agent):
    def move(self, state):
        """state is a dictionary representing the current game state."""

        # ... do something to read state ...

        move = {'type': 'stay', 'value': 1}
        return move
