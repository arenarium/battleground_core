from games.bunnies import dice_game

def test_init():
    state = {
          "rollable": [1]*dice_game.NUM_DICE,
          "bunnies": [0]*dice_game.NUM_DICE,
          "hutches": [0]*dice_game.NUM_DICE,
          "movable": [1]*dice_game.NUM_DICE,
          "currentPlayer": 0,
          "scores": {0:0},
          "extraBunnies": 0,
          "message": "",
          "allowedMoves": {"roll":1,"stay":0,"reset":0},
          "boardValue": 0
        }
    state_copy = state.copy()

    engine = dice_game.DiceGame(state)

    new_state = engine.move("roll")

    print(new_state)

    assert new_state!=state_copy


if __name__ == "__main__":
    test_init()
