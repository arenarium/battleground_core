
from games.basic_game.basic_game_engine import BasicGameEngine
from games.basic_game import basic_agent

from battleground.game_runner import GameRunner


def test_engine():
    bge = BasicGameEngine(num_players=2)
    assert len(bge.scores)==2
    assert bge.get_current_player()==0
    bge.move({"value":200})
    assert bge.get_current_player()!=0
    assert isinstance(bge.get_state(),dict)


def test_player():
    player = basic_agent.BasicAgent()
    move = player.move(None)
    assert isinstance(move,dict)
    assert "value" in move.keys()

def test_game():
    players = {}
    for i in range(3):
        players[i]=basic_agent.BasicAgent()
    engine = BasicGameEngine(num_players=3)
    runner = GameRunner(engine,players,save=False)
    scores = runner.run_game()
    print(engine.get_state())
    assert len(scores)==3
    assert all([x>=0 for x in scores])
    assert engine.turn > 1
