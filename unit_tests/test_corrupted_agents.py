from battleground.site_runner import start_session
import os


def test_corrupted_basic_agent():
    # there is some randomness in the initialisation, so try many times
    config_file = 'unit_tests/test_configurations/corrupted_basic_config.json'
    os.environ['DEBUG'] = 'True'
    exception = False
    try:
        start_session(config_file, save=False, run=True)
    except Exception as e:
        exception = True

    assert exception is True

    os.environ['DEBUG'] = 'False'
    # should not throw error
    start_session(config_file, save=False, run=True)


def test_corrupted_arena_agent():
    # there is some randomness in the initialisation, so try many times
    config_file = 'unit_tests/test_configurations/corrupted_arena_config.json'
    os.environ['DEBUG'] = 'True'
    exception = False
    try:
        start_session(config_file, save=False, run=True)
    except Exception as e:
        exception = True

    assert exception is True

    os.environ['DEBUG'] = 'False'
    # should not throw error
    start_session(config_file, save=False, run=True)
