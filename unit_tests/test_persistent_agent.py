import pytest
from battleground.persistence import game_data, agent_data
from battleground.games.basic_game.basic_persistent_agent import PersistentAgent
from battleground.games.basic_game.basic_game_engine import BasicGameEngine
from battleground import site_runner

owner, name, game_type = "test_owner", "test_name", "test_game_type"


@pytest.fixture(scope="module")
def db_handle():
    """temporary database for testing"""
    client = game_data.get_client()
    db_handle = game_data.get_db_handle("test_db_handle")
    yield db_handle
    client.drop_database("test_db_handle")


def test_memory_set():
    for entry in [2, 5, 6, "5", [12, 3, 5], None, 5.6]:
        agent = PersistentAgent()
        agent.set_memory({"guess": entry})
        assert agent.get_memory()["guess"] == entry


def test_move():
    agent = PersistentAgent()
    move = agent.move(state={"turn": 5})
    assert move["value"] == agent.default_mem["guess"]


def test_observe():
    agent = PersistentAgent()
    agent.observe(state={"turn": 5})
    assert agent.get_memory()["guess"] == agent.default_mem["guess"]


def test_with_engine():
    game_type = "test_game"
    num_players = 4
    players = []
    player_mems = {}

    # create agents
    for i in range(num_players):
        owner = "core"
        name = "basic_persistent_{}".format(i)
        agent_id = agent_data.get_agent_id(owner, name, game_type)
        players.append((str(agent_id), PersistentAgent()))

    # run games
    for game_num in range(2):
        engine = BasicGameEngine(num_players=num_players, type=game_type)

        scores = site_runner.run_session(engine, players, 4, save=True)
        assert len(scores) == num_players

        for agent_id, player in players:
            db_memory = agent_data.load_agent_data(agent_id, "memory")
            assert isinstance(db_memory, dict)

            memory = player.get_memory()

            assert db_memory == memory

            if agent_id in player_mems:
                player_mems[agent_id].append(player.get_memory())
            else:
                player_mems[agent_id] = [player.get_memory()]

    #  check that memory after game 1 is different from memory after game 2.
    for _, mem in player_mems.items():
        assert mem[0] != mem[1]


def test_unique_owner_name_type():
    owners = agent_data.get_owners()
    all_ids = []
    for owner in owners:
        assert len(owners) > 0
        agents = agent_data.get_agents(owner)
        assert len(agents) > 0
        names_types = set()
        for agent in agents:
            if type(agent["game_type"]) == list:
                game_type = agent["game_type"][0]
            else:
                game_type = agent["game_type"]
            names_types.add((agent["name"], game_type))
            all_ids.append(str(agent["_id"]))
        assert len(names_types) == len(agents)
        assert len(all_ids) == len(set(all_ids))
