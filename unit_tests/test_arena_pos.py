from battleground.site_runner import start_session


def test_arena_postion():
    # there is some randomness in the initialisation, so try many times
    for i in range(10):
            config_file = 'unit_tests/test_configurations/arena_pos_test_config.json'
            agents, engine = start_session(config_file, save=False, run=False)
            game_state = engine.get_state()
            keys = ['gladiators', 'move_options', 'dungeon', 'queue', 'message', 'scores']
            for key in keys:
                assert key in game_state
            types = [x['type'] for x in game_state['move_options']]
            if 'move' not in types:
                print(game_state)
            assert 'move' in types
            assert 'stay' in types
