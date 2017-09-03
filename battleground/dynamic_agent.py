
from . import agent
import importlib
import sys, inspect

class DynamicAgent(agent.Agent):

    def __init__(self,
                 owner,
                 name,
                 local_path=None,
                 queue_prefix=None,
                 **kwargs):

        if local_path is not None:
            agent_module = importlib.import_module(local_path)
            for name, obj in inspect.getmembers(agent_module):
                if inspect.isclass(obj):
                    agent_class = obj
            self.agent_instance = agent_class(**kwargs["settings"])
        elif queue_prefix is not None:
            raise NotImplementedError()

    def move(self,state):
        return self.agent_instance.move(state)
