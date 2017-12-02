from .persistence import game_data, agent_data
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
        state = self.game_engine.get_save_state()
        self.game_states.append({"game_state": state,
                                 "last_move": None,
                                 "player_ids": self.player_ids
                                 })

        player_index = self.game_engine.get_current_player()

        while not self.game_engine.game_over():
            engine_state = self.game_engine.get_state()
            move = self.players[player_index].move(engine_state)
            self.game_engine.move(move)
            state = self.game_engine.get_save_state()

            data_to_save = {}
            data_to_save["game_state"] = copy.deepcopy(state)
            data_to_save["last_move"] = copy.deepcopy(move)
            data_to_save["player_ids"] = copy.deepcopy(self.player_ids)

            self.game_states.append(data_to_save)
            self.broadcast(data_to_save)
            player_index = self.game_engine.get_current_player()

        # the final scores
        scores = self.game_engine.get_state()["scores"]

        if self.save:
            # save game states and player stats to the DB.
            game_id = game_data.save_game_history(
                self.game_engine.get_game_name(), self.game_states)
            for i in range(len(self.players)):
                player = self.players[i]
                agent_id = self.player_ids[i]
                score = scores[i]
                agent_data.save_game_result(agent_id, game_id,
                                            self.game_engine.type,
                                            score,
                                            max(scores) == score)

        return scores

    def broadcast(self, state):
        pass
