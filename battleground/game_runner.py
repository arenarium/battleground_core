from .persistence import game_data, agent_data
import copy


class GameRunner(object):
    def __init__(self, game_engine, agent_objects, save=True):
        self.game_engine = game_engine
        self.agent_ids, self.players = zip(*agent_objects)
        self.game_states = []
        self.save = save

    def run_game(self):
        # self.game_engine.reset()
        state = self.game_engine.get_state()
        self.game_states.append({"game_state": state,
                                 "last_move": None,
                                 "player_ids": self.agent_ids
                                 })

        player_index = self.game_engine.get_current_player()

        while not self.game_engine.game_over():
            engine_state = self.game_engine.get_state(player_index)

            engine_state['current_player'] = player_index

            move = self.players[player_index].move(engine_state)
            self.game_engine.move(move)

            state = self.game_engine.get_state()
            player_index = self.game_engine.get_current_player()

            data_to_save = {}
            data_to_save["game_state"] = copy.deepcopy(state)
            data_to_save["last_move"] = copy.deepcopy(move)
            data_to_save["player_ids"] = copy.deepcopy(self.agent_ids)
            data_to_save["game_state"]["game_over"] = str(self.game_engine.game_over())
            data_to_save["game_state"]['current_player'] = player_index

            self.game_states.append(data_to_save)
            self.broadcast(data_to_save)



        # the final scores
        scores = self.game_engine.get_state()["scores"]
        if self.save:
            # save game states and player stats to the DB.
            game_id = game_data.save_game_history(self.game_engine.get_game_name(),
                                                  self.game_states)
            for index, agent_id in enumerate(self.agent_ids):
                score = scores[index]
                agent_data.save_game_result(agent_id, game_id,
                                            self.game_engine.type,
                                            score,
                                            max(scores) == score)

        return scores

    def broadcast(self, data):
        state = data["game_state"]
        for player in self.players:
            player.observe(state)
