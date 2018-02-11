
from battleground.games.basic_game.basic_game_engine import BasicGameEngine
from battleground.games.basic_game import basic_agent

from battleground.game_runner import GameRunner


def test_engine():
    bge = BasicGameEngine(num_players=2, type="bg")
    assert len(bge.scores) == 2
    assert bge.get_current_player() == 0
    bge.move({"value": 200})
    assert bge.get_current_player() != 0
    assert isinstance(bge.get_state(), dict)
    assert bge.get_game_name() == "bg"


def test_player():
    bge = BasicGameEngine(num_players=2, type="bg")
    player = basic_agent.BasicAgent()
    move = player.move(bge.get_state())
    assert isinstance(move, dict)
    assert "value" in move.keys()


def test_game():
    players = []
    for i in range(3):
        players.append((i, basic_agent.BasicAgent()))
    engine = BasicGameEngine(num_players=3, type="bg")
    runner = GameRunner(engine, players, save=False)
    scores = runner.run_game()
    print(engine.get_state())
    assert len(scores) == 3
    assert all([x >= 0 for x in scores])
    assert engine.turn > 1

    for i, state in enumerate(runner.game_states):
        for key in ["game_state", "player_ids", "last_move"]:
            assert key in state

        assert isinstance(state["game_state"], dict)
        assert isinstance(state["player_ids"], tuple)
        if i == 0:
            assert state["last_move"] is None
        else:
            assert isinstance(state["last_move"], dict)
