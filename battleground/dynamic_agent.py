from . import agent
import importlib
import sys
import inspect


class DynamicAgent(agent.Agent):
    def __init__(self,
                 owner,
                 name,
                 local_path=None,
                 queue_prefix=None,
                 **kwargs):
        super().__init__()

        if local_path is not None:
            agent_module = importlib.import_module(local_path)
            for name, obj in inspect.getmembers(agent_module):
                # May not pick the correct class if other classes are imported directly into agent_module!
                if inspect.isclass(obj):
                    agent_class = obj
            if "settings" in kwargs:
                self.agent_instance = agent_class(**kwargs["settings"])
            else:
                self.agent_instance = agent_class()
        elif queue_prefix is not None:
            raise NotImplementedError()

    def move(self, state):
        return self.agent_instance.move(state)

    def observe(self, state):
        raise NotImplementedError()
