from battleground import config_generator
from battleground.persistence import agent_data
import os.path

BASE_PATH = os.path.join(os.path.dirname(__file__), '../..')
DEFAULT_CONFIG_PATH = os.path.join(BASE_PATH, "battleground/config/initial_db_agents.json")


def add_default_players():
    players = config_generator.generate_players_config_from_file(DEFAULT_CONFIG_PATH)

    for name, player in players.items():
        assert name == player['name']
        local_path = player['local_path'].replace('.', '/') + ".py"
        if not os.path.isfile(local_path):
            local_path = os.path.join(BASE_PATH, local_path)
        assert os.path.isfile(local_path)
        with open(local_path, 'r') as file:
            code = file.read()

        for game_type in player['game_type']:
            agent_data.save_agent_code(owner=player['owner'],
                                       name=player['name'],
                                       game_type=game_type,
                                       code=code)


if __name__ == '__main__':
    add_default_players()
