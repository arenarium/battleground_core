from . import agent
import importlib
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
                 class_name=None,
                 from_db=False,
                 local_path=None,
                 queue_prefix=None,
                 settings=None,
                 **kwargs):
        self.owner = owner
        self.name = name
        self.game_type = game_type
        self.class_name = class_name
        self.local_path = local_path
        self.settings = settings
        if "agent_id" in kwargs:
            self.agent_id = kwargs["agent_id"]
        else:
            self.agent_id = agent_data.get_agent_id(owner=self.owner,
                                                    name=self.name,
                                                    game_type=self.game_type)

        if not os.path.exists(TEMP_MODULE_PATH):
            os.mkdir(TEMP_MODULE_PATH)

        if from_db:
            self.agent_instance = self._load_from_database()
        elif local_path is not None:
            self.agent_instance = self._load_from_file()
        elif queue_prefix is not None:
            raise NotImplementedError()

        super().__init__()

    def _load_from_database(self):
        """
        Load agent code from the database, then save as a file.
        """

        code_string = agent_data.load_agent_data(self.agent_id, "code")

        if code_string is None:
            error_message = "No code found in database for owner: {}, name: {}, type: {}"
            error_message = error_message.format(self.owner,
                                                 self.name,
                                                 self.game_type)
            raise Exception(error_message)

        # generate random temporary file name
        file_name = "m_{}.py".format(random.randint(1e8, 2e8))
        module_path = os.path.join(TEMP_MODULE_PATH, file_name)

        # write to temp file
        with open(module_path, 'w') as file:
            file.write(code_string)

        importlib.invalidate_caches()
        # change path to module specifier
        self.local_path = module_path[:-3].replace("/", ".")

        # load the module
        return self._load_from_file()

    def _load_from_file(self):
        """loads agent code from a file specified at runtime"""

        agent_class = None
        agent_module = importlib.import_module(self.local_path)
        for name, obj in inspect.getmembers(agent_module):
            if name == self.class_name and inspect.isclass(obj):
                agent_class = obj

        if agent_class is None:
            raise Exception("agent class '{}' not found in {}.".format(self.class_name, self.local_path))

        if self.settings is not None:
            return agent_class(**self.settings)
        else:
            return agent_class()

    def move(self, state):
        return self.agent_instance.move(state)

    def observe(self, state):
        return self.agent_instance.observe(state)

    def get_memory(self, **kwargs):
        return self.agent_instance.get_memory()

    def set_memory(self, data):
        return self.agent_instance.set_memory(data)
