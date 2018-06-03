from battleground import config_generator
from battleground.persistence import agent_data
import os.path

DEFAULT_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "../config/initial_db_agents.json")

players = config_generator.generate_players_config_from_file(DEFAULT_CONFIG_PATH)

for name, player in players.items():
    assert name == player['name']
    local_path = player['local_path'].replace('.', '/') + ".py"
    with open(local_path, 'r') as file:
        code = file.read()

    agent_data.save_agent_code(owner=player['owner'],
                               name=player['name'],
                               game_type=player['game_type'][0],
                               code=code)
