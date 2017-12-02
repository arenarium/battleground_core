from . import agent
import importlib
import sys
import inspect
from .persistence import agent_data
import random
import os

TEMP_MODULE_PATH = "tmp/"


class DynamicAgent(agent.Agent):
    def __init__(self,
                 owner,
                 name,
                 game_type=None,
                 from_db=False,
                 local_path=None,
                 queue_prefix=None,
                 settings=None,
                 **kwargs):
        super().__init__()
        self.owner = owner
        self.name = name
        self.game_type = game_type
        self.local_path = local_path
        self.settings = settings

        if not os.path.exists(TEMP_MODULE_PATH):
            os.mkdir(TEMP_MODULE_PATH)

        if from_db:
            self.agent_instance = self._load_from_database()
        elif local_path is not None:
            self.agent_instance = self._load_from_file()
        elif queue_prefix is not None:
            raise NotImplementedError()

    def _load_from_database(self):
        agent_id = agent_data.get_agent_id(owner=self.owner,
                                           name=self.name,
                                           game_type=self.game_type)
        code_string = agent_data.load_agent_data(agent_id, "code")
        if code_string is not None:
            module_path = os.path.join(
                TEMP_MODULE_PATH, "m_{}.py".format(
                    random.randint(
                        1e5, 2e5)))
            with open(module_path, 'w') as f:
                f.write(code_string)
            self.local_path = module_path[:-3].replace("/", ".")
            return self._load_from_file()

    def _load_from_file(self):
        agent_module = importlib.import_module(self.local_path)
        for name, obj in inspect.getmembers(agent_module):
            # May not pick the correct class if other classes are imported
            # directly into agent_module!
            if inspect.isclass(obj):
                agent_class = obj
        if self.settings is not None:
            return agent_class(**self.settings)
        else:
            return agent_class()

    def move(self, state):
        return self.agent_instance.move(state)

    def observe(self, state):
        raise NotImplementedError()
