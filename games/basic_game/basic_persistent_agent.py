from battleground.agent import Agent


class BasicAgent(Agent):
    def __init__(self, data=None):
        super().__init__()
        if data is None:
            self.data = {"guess": 5}
        else:
            self.data = data

    def move(self, state):
        return {"value": self.data["guess"]}

    def observe(self, state):
        raise NotImplementedError()

    def get_data_to_save(self):
        """
        the value returned here will be passed as the "data" parameter on the
        next initialization of the agent.
        """
        return self.data
