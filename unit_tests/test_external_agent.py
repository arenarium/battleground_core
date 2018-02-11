from battleground.persistence import agent_data
from battleground.utils import start
from battleground import site_runner

config = {
    "owner": "test_owner",
    "name": "test_agent",
    "game_type": "basic_game_50",
    "local_path": None,
    "remote_path": "battleground/games/basic_game/basic_persistent_agent.py",
    "class_name": "PersistentAgent"
}


def test_play():
    players = {}

    with open(config["remote_path"], 'r') as file:
        code = file.read()

    for i in range(4):
        agent_id = agent_data.save_agent_code(owner=config["owner"],
                                              name="{}_{}".format(config["name"], i),
                                              game_type=config["game_type"],
                                              code=code)
        config_temp = config.copy()
        config_temp["name"] = "{}_{}".format(config["name"], i)
        config_temp["from_db"] = True
        players[str(agent_id)] = config_temp

    game_config = start.generate_dynamic_config(game_delay=None,
                                                game_name="Basic Game 50",
                                                players=list(players.values()))
    scores = site_runner.start_session(game_config)

    assert len(scores) > 0

    for agent_id, players_config in players.items():
        memory = agent_data.load_agent_data(agent_id, "memory")
        assert memory is not None
