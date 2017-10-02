from .persistence import game_data
import copy


class GameRunner(object):
    def __init__(self, game_engine, players, save=True):
        self.game_engine = game_engine
        self.players = list(players.values())
        self.player_ids = list(players.keys())
        self.game_states = []
        self.save = save

    def run_game(self):
        # self.game_engine.reset()
        state = self.game_engine.get_state()
        save_state = self.game_engine.decode_state(state)
        self.game_states.append({"game_state": save_state,
                                 "last_move": None,
                                 "player_ids": self.player_ids
                                 })

        player_index = self.game_engine.get_current_player()

        while not self.game_engine.game_over():
            state = self.game_engine.get_state()
            move = self.players[player_index].move(state)
            self.game_engine.move(move)

            save_state = self.game_engine.decode_state(state)
            save_move = self.game_engine.decode_move(move)

            data_to_save = {}
            data_to_save["game_state"] = copy.deepcopy(save_state)
            data_to_save["last_move"] = copy.deepcopy(save_move)
            data_to_save["player_ids"] = copy.deepcopy(self.player_ids)

            self.game_states.append(data_to_save)
            self.broadcast(data_to_save)
            player_index = self.game_engine.get_current_player()

        if self.save:
            game_data.save_game_history(self.game_engine.get_game_name(),
                                        self.game_states)
        return self.game_engine.get_state()["scores"]

    def broadcast(self, state):
        pass
