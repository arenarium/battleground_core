from battleground.agent import Agent


class BasicAgent(Agent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def move(self, state):
        move = {}
        # RuntimeError
        new_var = move['hello']

        print(new_var)
        return move
