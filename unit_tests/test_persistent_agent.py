import pytest
from battleground.persistence import game_data, agent_data
from games.basic_game.basic_persistent_agent import PeristentAgent
from games.basic_game.basic_game_engine import BasicGameEngine
from battleground import site_runner

owner, name, game_type = "test_owner", "test_name", "test_game_type"


@pytest.fixture(scope="module")
def db_handle():
    """temporary database for testing"""
    c = game_data.get_client()
    db_handle = game_data.get_db_handle("test_db_handle")
    yield db_handle
    c.drop_database("test_db_handle")


def test_memory_set():
    for x in [2, 5, 6, "5", [12, 3, 5], None, 5.6]:
        agent = PeristentAgent()
        agent.set_memory({"guess": x})
        assert agent.get_memory()["guess"] == x


def test_move():
    agent = PeristentAgent()
    move = agent.move(state={"turn": 5})
    assert move["value"] == agent.default_mem["guess"]


def test_observe():
    agent = PeristentAgent()
    agent.observe(state={"turn": 5})
    assert agent.get_memory()["guess"] == agent.default_mem["guess"]


def test_with_engine():
    game_type = "test_game"
    num_players = 4
    players = {}
    player_mems = {}
    for game_num in range(2):
        engine = BasicGameEngine(num_players=num_players, type=game_type)

        for i in range(num_players):
            owner = "core"
            name = "basic_persistent_{}".format(i)
            agent_id = agent_data.get_agent_id(owner, name, game_type)
            players[str(agent_id)] = PeristentAgent()

        scores = site_runner.run_session(engine, players, 4, save=True)
        assert len(scores) > 0

        for agent_id, player in players.items():
            db_memory = agent_data.load_agent_data(agent_id, "memory")
            assert isinstance(db_memory, dict)

            memory = player.get_memory()

            assert db_memory == memory

            if agent_id in player_mems:
                player_mems[agent_id].append(player.get_memory())
            else:
                player_mems[agent_id] = [player.get_memory()]

    for id, mem in player_mems.items():
        assert mem[0] != mem[1]
