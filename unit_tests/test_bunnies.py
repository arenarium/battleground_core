from games.bunnies import dice_game
import random
import copy


def test_init():
    num_players = 2

    state = {
        "rollables": [1] * dice_game.NUM_DICE,
        "bunnies": [0] * dice_game.NUM_DICE,
        "hutches": [0] * dice_game.NUM_DICE,
        "movables": [1] * dice_game.NUM_DICE,
        "currentPlayer": 0,
        "scores": {0: 0},
        "extraBunnies": 0,
        "message": "",
        "allowedMoves": {"roll": 0, "stay": 0, "reset": 0, "moveBunny": 1, "moveHutch": 1},
        "boardValue": 0,
        "lastPlayer": num_players,
        "lastRound": False
    }

    engine = dice_game.DiceGame(state)

    # check name
    assert engine.get_game_name() == "Bunnies"

    engine.reset()

    # check reset properties
    assert state["bunnies"] == [0] * dice_game.NUM_DICE
    assert state["hutches"] == [0] * dice_game.NUM_DICE
    assert state["movables"] == [1] * dice_game.NUM_DICE
    assert state["currentPlayer"] == 0
    assert state["scores"] == {0: 0}
    assert state["extraBunnies"] == 0
    assert state["message"] == ""
    assert (state["allowedMoves"] == {"roll": 0, "stay": 1, "reset": 0, "moveBunny": 0, "moveHutch": 0}
            or state["allowedMoves"] == {"roll": 0, "stay": 0, "reset": 0, "moveBunny": 1, "moveHutch": 1})
    assert state["boardValue"] == 0
    assert state["lastPlayer"] == num_players
    assert state["lastRound"] is False

    # create state without hutches
    state["rollables"] = [1] * dice_game.NUM_DICE
    # try to move a die into the hutch container
    engine.move(["moveHutch", random.randint(0, dice_game.NUM_DICE - 1)])
    # check that bunnies didn't move into hutches container:
    assert state["hutches"] == [0] * dice_game.NUM_DICE

    # create state without bunnies or correct hutches (2 needs to be the first)
    state["rollables"] = [random.randint(3, 6) for x in state["rollables"]]
    # try to move a die into the bunny container
    engine.move(["moveBunny", random.randint(0, dice_game.NUM_DICE - 1)])
    # check that hutch didn't move into bunnies container:
    assert state["bunnies"] == [0] * dice_game.NUM_DICE
    # try to move a die into the hutch container
    engine.move(["moveHutch", random.randint(0, dice_game.NUM_DICE - 1)])
    # check that die didn't move into hutches container
    assert state["hutches"] == [0] * dice_game.NUM_DICE

    # create state with only bunnies
    state["rollables"] = [random.randint(1, 2) for x in state["rollables"]]
    # try to move a die into the bunny container
    engine.move(["moveBunny", random.randint(0, dice_game.NUM_DICE - 1)])
    # check that bunny did move into bunnies container:
    assert state["bunnies"].count(0) == dice_game.NUM_DICE - 1
    # check that moving a bunny enabled stay move as allowed move
    assert state["allowedMoves"]["stay"] == 1

    engine.reset()

    # create state with only 2-hutches
    state["rollables"] = [2] * dice_game.NUM_DICE
    # try to move a die into the hutch container
    engine.move(["moveHutch", random.randint(0, dice_game.NUM_DICE - 1)])
    # check that hutch did move into hutch container:
    assert state["hutches"].count(0) == dice_game.NUM_DICE - 1

    engine.reset()

    # set a state
    state["rollables"] = [0] * dice_game.NUM_DICE
    state["bunnies"] = [1] * dice_game.NUM_DICE
    state["movables"] = [0] * dice_game.NUM_DICE
    state["allowedMoves"] = {"roll": 1, "stay": 1, "reset": 0, "moveBunny": 1, "moveHutch": 1}

    engine.move(["roll", 0])
    # check if all dice from bunnies were used as rollables
    assert state["rollables"].count(0) == 0
    assert state["bunnies"] == [0] * dice_game.NUM_DICE
    assert state["extraBunnies"] == (dice_game.NUM_DICE // 2) * 10 + dice_game.NUM_DICE % 2
    assert state["allowedMoves"]["roll"] == 0
    assert state["allowedMoves"]["reset"] == 0

    state_copy = copy.deepcopy(state)

    # check consecutiveness of hatches
    # check consecutiveness of players
    # check roll move
    # check stay move: taking over state from previous player and continue playing
    # check reset move
    # check scoring
    # check ending condition
    # check carrots


if __name__ == "__main__":
    test_init()



    # state = {"rollables": [1] * dice_game.NUM_DICE, "bunnies": [0] * dice_game.NUM_DICE, "hutches": [0] * dice_game.NUM_DICE, "movables": [1] * dice_game.NUM_DICE, "currentPlayer": 0, "scores": {0:0}, "extraBunnies": 0, "message": "", "allowedMoves": {"roll": 0, "stay": 0, "reset": 0, "moveBunny": 1, "moveHutch": 1}, "boardValue": 0,"lastPlayer": 2, "lastRound": False}
