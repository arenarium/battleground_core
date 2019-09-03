import pytest
import json
from battleground import site_runner, config_generator

PLAYERS_PATH = "battleground/config/initial_db_agents.json"


def get_game_configs():
    with open("battleground/config/registered_games_production.json") as file:
        registered_games = json.load(file)
    return registered_games


@pytest.mark.parametrize("game_spec", get_game_configs())
def test_games(game_spec):
    config = config_generator.generate_dynamic_config([game_spec], players=PLAYERS_PATH)
    game_engine = site_runner.game_engine_factory(3, game_spec)

    state = game_engine.get_state()
    assert isinstance(state, dict)

    players = site_runner.assign_agents(config['players'], game_type=game_spec['type'], save=False)
    players = [x[1] for x in players]

    game_engine.move(players[0].move(state))
    new_state = game_engine.get_state()

    assert isinstance(new_state, dict)
    assert new_state != state

    game_engine.move({})
    new_state = game_engine.get_state()

    assert isinstance(new_state, dict)
