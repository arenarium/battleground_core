import json
import os
from battleground import dynamic_agent

CONFIG_PATH = 'battleground/config/initial_db_agents.json'

os.environ['DEBUG'] = 'True'


def test_initial_db_agents():
    with open(CONFIG_PATH, 'r') as file:
        config = json.load(file)

    for name, agent in config.items():
        agent['agent_id'] = 0
        agent = dynamic_agent.DynamicAgent(**agent, save=False)
        assert agent.name == name
