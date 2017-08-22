from games.bunnies import dice_game


def test_init():
    num_players = 2

    state = {
        "rollables": [1] * dice_game.NUM_DICE,
        "bunnies": [0] * dice_game.NUM_DICE,
        "hutches": [0] * dice_game.NUM_DICE,
        "movables": [1] * dice_game.NUM_DICE,
        "currentPlayer": 0,
        "scores": {0:0},
        "extraBunnies": 0,
        "message": "",
        "allowedMoves": {"roll": 0, "stay": 0, "reset": 0, "moveBunny": 1, "moveHutch": 1},
        "boardValue": 0,
        "lastPlayer": num_players,
        "lastRound": False
    }

    state_copy = state.copy()

    engine = dice_game.DiceGame(state)

    new_state = engine.move(["roll", 0])

    print(new_state)

    assert new_state != state_copy


if __name__ == "__main__":
    test_init()



# state = {"rollables": [1] * dice_game.NUM_DICE, "bunnies": [0] * dice_game.NUM_DICE, "hutches": [0] * dice_game.NUM_DICE, "movables": [1] * dice_game.NUM_DICE, "currentPlayer": 0, "scores": {0:0}, "extraBunnies": 0, "message": "", "allowedMoves": {"roll": 0, "stay": 0, "reset": 0, "moveBunny": 1, "moveHutch": 1}, "boardValue": 0,"lastPlayer": 2, "lastRound": False}