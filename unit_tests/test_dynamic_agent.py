from battleground.dynamic_agent import DynamicAgent


def test_dynamic_agent():
    config={
        "owner":"test_owner",
        "name":"test_agent",
        "local_path":"games.basic_game.basic_agent",
        "remote_path":None
        }

    da = DynamicAgent(**config)

    assert isinstance(da.move(None),dict)
