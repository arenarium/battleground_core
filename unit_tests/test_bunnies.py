from games.bunnies import dice_game
import random
import copy


num_players = 2

# state = {"rollables": [1] * dice_game.NUM_DICE, "bunnies": [0] * dice_game.NUM_DICE, "hutches": [0] * dice_game.NUM_DICE, "movables": [1] * dice_game.NUM_DICE, "currentPlayer": 0, "scores": {0:0}, "extraBunnies": 0, "message": "", "allowedMoves": {"roll": 0, "stay": 0, "reset": 0, "moveBunny": 1, "moveHutch": 1}, "boardValue": 0,"lastPlayer": 2, "lastRound": False}

STATE = {
    "rollables": [1] * dice_game.NUM_DICE,
    "bunnies": [0] * dice_game.NUM_DICE,
    "hutches": [0] * dice_game.NUM_DICE,
    "movables": [1] * dice_game.NUM_DICE,
    "currentPlayer": 0,
    "scores": {0: 0},
    "extraBunnies": 0,
    "message": "",
    "allowedMoves": {"roll": 0, "stay": 0, "reset": 0, "moveBunny": 1, "moveHutch": 0},
    "boardValue": 0,
    "lastPlayer": num_players,
    "lastRound": False
}


def test_reset():
    for state in [STATE,None]:
        engine = dice_game.DiceGame(num_players=2, type="Bunnies", state=state)
        engine.reset()
        state = copy.deepcopy(engine.get_state())
        # check reset properties
        assert state["rollables"].count(0) == 0
        assert state["bunnies"] == [0] * dice_game.NUM_DICE
        assert state["hutches"] == [0] * dice_game.NUM_DICE
        assert state["movables"] == [1] * dice_game.NUM_DICE
        assert state["currentPlayer"] == 0
        for key, value in state["scores"].items():
            assert value == 0
        assert state["extraBunnies"] == 0
        assert state["message"] == ""
        assert (state["allowedMoves"] == {"roll": 0, "stay": 1, "reset": 0, "moveBunny": 0, "moveHutch": 0}
                or state["allowedMoves"] == {"roll": 0, "stay": 0, "reset": 0, "moveBunny": 1, "moveHutch": 0})
        assert state["boardValue"] == 0
        assert state["lastPlayer"] == num_players
        assert not state["lastRound"]


def test_score():
    engine = dice_game.DiceGame(num_players=2, type="Bunnies", state=STATE)
    engine.reset()
    state = copy.deepcopy(engine.get_state())
    # create state to check scoring
    state["rollables"] = [0] * dice_game.NUM_DICE
    state["bunnies"] = [1, 1, 1, 2, 0, 0, 0]
    state["hutches"] = [0, 0, 0, 0, 2, 3, 4]
    state["movables"] = [0] * dice_game.NUM_DICE
    state["extraBunnies"] = 43
    state["allowedMoves"] = {"roll": 1, "stay": 1, "reset": 0, "moveBunny": 0, "moveHutch": 0}
    engine.move({"name": "stay",
                 "value": 0})
    assert 0 in state["scores"]
    assert state["scores"][0] == 43 + (10 + 3) * 4
    assert state["boardvalue"] == 43 + (10 + 3) * 4
    engine.move({"name": "reset",
                 "value": 0})
    assert state["extraBunnies"] == 0
    if state["allowedMoves"]["moveBunny"] == 1:
        state["rollables"] = [6, 1, 2, 4, 5, 5, 6]
        engine.move({"name": "moveBunny",
                     "value": 1})
    engine.move({"name": "stay",
                 "value": 0})
    assert 1 in state["scores"]
    assert state["scores"][1] <= 1


def test_do_roll():
    engine = dice_game.DiceGame(num_players=num_players, type="Bunnies", state=STATE)
    engine.reset()
    state = copy.deepcopy(engine.get_state())
    # set a state with only bunnies, no rollables
    state["rollables"] = [0] * dice_game.NUM_DICE
    state["bunnies"] = [1] * dice_game.NUM_DICE
    state["movables"] = [0] * dice_game.NUM_DICE
    state["allowedMoves"] = {"roll": 1, "stay": 1, "reset": 0, "moveBunny": 1, "moveHutch": 1}
    current_player = state["currentPlayer"]
    engine.move({"name": "roll",
                 "value": 0})
    # check if all dice from bunnies were used as rollables
    assert state["rollables"].count(0) == 0
    assert state["bunnies"] == [0] * dice_game.NUM_DICE
    assert state["extraBunnies"] == (dice_game.NUM_DICE // 2) * 10 + dice_game.NUM_DICE % 2
    assert state["allowedMoves"]["roll"] == 0
    assert state["allowedMoves"]["reset"] == 0
    # check if player stays the same
    assert state["currentPlayer"] == current_player


def test_do_stay():
    # check stay move: taking over state from previous player and continue playing
    assert True


def test_do_reset():
    engine = dice_game.DiceGame(num_players=num_players, type="Bunnies", state=STATE)
    engine.reset()
    state = copy.deepcopy(engine.get_state())
    # set a state that was just passed on
    state["rollables"] = [0, 5, 4, 6, 0, 4, 0]
    state["bunnies"] = [1, 0, 0, 0, 1, 0, 0]
    state["movables"] = [0, 0, 0, 0, 0, 0, 2]
    state["allowedMoves"] = {"roll": 1, "stay": 0, "reset": 1, "moveBunny": 0, "moveHutch": 0}
    current_player = state["currentPlayer"]
    engine.move({"name": "reset",
                 "value": 0})
    assert state["rollables"].count(0) == 0
    assert state["bunnies"] == [0] * dice_game.NUM_DICE
    assert state["hutches"] == [0] * dice_game.NUM_DICE
    assert state["movables"] == [1] * dice_game.NUM_DICE
    assert state["currentPlayer"] == current_player
    assert state["extraBunnies"] == 0
    assert (state["allowedMoves"] == {"roll": 0, "stay": 1, "reset": 0, "moveBunny": 0, "moveHutch": 0}
            or state["allowedMoves"] == {"roll": 0, "stay": 0, "reset": 0, "moveBunny": 1, "moveHutch": 1})
    assert state["boardValue"] == 0


def test_move_bunnies():
    # create state without bunnies or correct hutches (2 needs to be the first hutch)
    engine = dice_game.DiceGame(num_players=num_players, type="Bunnies", state=STATE)
    engine.reset()
    state = copy.deepcopy(engine.get_state())
    state["rollables"] = [random.randint(3, 6) for x in state["rollables"]]
    # try to move a die into the bunny container
    engine.move({"name": "moveBunny",
                 "value": random.randint(0, dice_game.NUM_DICE - 1)})
    # check that hutch didn't move into bunnies container:
    assert state["bunnies"] == [0] * dice_game.NUM_DICE
    # check that allowed moves didn't change
    assert state["allowedMoves"] == {"roll": 0, "stay": 0, "reset": 0, "moveBunny": 1, "moveHutch": 1}

    # create state with only bunnies
    state["rollables"] = [random.randint(1, 2) for x in state["rollables"]]
    # try to move a die into the bunny container
    engine.move({"name": "moveBunny",
                 "value": random.randint(0, dice_game.NUM_DICE - 1)})
    # check that bunny did move into bunnies container:
    assert state["bunnies"].count(0) == dice_game.NUM_DICE - 1
    # check that moving a bunny enabled stay move as allowed move
    assert state["allowedMoves"]["stay"] == 1


def test_move_hutches():
    # create state without hutches
    engine = dice_game.DiceGame(num_players=num_players, type="Bunnies", state=STATE)
    engine.reset()
    state = copy.deepcopy(engine.get_state())
    state["rollables"] = [1] * dice_game.NUM_DICE
    # try to move a die into the hutch container
    engine.move({"name": "moveHutch",
                 "value": random.randint(0, dice_game.NUM_DICE - 1)})
    # check that bunnies didn't move into hutches container:
    assert state["hutches"] == [0] * dice_game.NUM_DICE

    # create state without correct hutches (2 needs to be the first hutch)
    state["rollables"] = [random.randint(3, 6) for x in state["rollables"]]
    # try to move a die into the hutch container
    engine.move({"name": "moveHutch",
                 "value": random.randint(0, dice_game.NUM_DICE - 1)})
    # check that die didn't move into hutches container
    assert state["hutches"] == [0] * dice_game.NUM_DICE

    # create state with only 2-hutches
    state["rollables"] = [2] * dice_game.NUM_DICE
    # try to move a die into the hutch container
    engine.move({"name": "moveHutch",
                 "value": random.randint(0, dice_game.NUM_DICE - 1)})
    # check that hutch did move into hutch container:
    assert state["hutches"].count(0) == dice_game.NUM_DICE - 1


def test_last_round():
    # check ending condition
    engine = dice_game.DiceGame(num_players=2, type="Bunnies", state=STATE)
    engine.reset()
    state = copy.deepcopy(engine.get_state())
    # set a state that leads to END_SCORE, triggering the last round
    player_0 = state["currentPlayer"]
    state["rollables"] = [6, 1, 2, 4, 5, 5, 6]
    state["allowedMoves"] = {"roll": 0, "stay": 0, "reset": 0, "moveBunny": 1, "moveHutch": 1}
    state["scores"][player_0] = dice_game.END_SCORE - 1
    engine.move({"name": "moveBunny",
                 "value": 1})
    engine.move({"name": "stay",
                 "value": 0})
    print(state["scores"])
    assert state["scores"][player_0] == dice_game.END_SCORE
    assert state["lastRound"]
    assert state["lastPlayer"] == player_0
    engine.move({"name": "reset",
                 "value": 0})
    if state["allowedMoves"]["moveBunny"] == 1:
        state["rollables"] = [6, 1, 2, 4, 5, 5, 6]
        engine.move({"name": "moveBunny",
                     "value": 1})
    engine.move({"name": "stay",
                 "value": 0})
    assert state["lastRound"]
    assert state["lastPlayer"] == player_0
    assert state["allowedMoves"] == {"roll": 0, "stay": 0, "reset": 0, "moveBunny": 0, "moveHutch": 0}


def test_game_over():
    assert True

    # check consecutiveness of hatches
    # check consecutiveness of players
    # check carrots


if __name__ == "__main__":
    test_reset()
    test_score()
    test_do_roll()
    test_do_stay()
    test_do_reset()
    test_move_bunnies()
    test_move_hutches()
    test_last_round()
    test_game_over()
