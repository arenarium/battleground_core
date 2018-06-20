from battleground.agent import Agent


class PersistentAgent(Agent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.default_mem = {"guess": 5}

    def move(self, state):
        memory = self.get_memory(default=self.default_mem)
        # do something with memory here
        my_move = {"value": memory["guess"]}

        # update memory
        memory['key 1'] = 'value _1'
        memory['key 2'] = 'value _2'
        self.set_memory(memory)

        # return move
        return my_move
