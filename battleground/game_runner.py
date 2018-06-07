from .persistence import game_data, agent_data
import copy
from datetime import datetime
# turn stages:
# - current player recieves its view on the game state
# - player makes a move
# - move is resolved
# - state after move is broadcast
# - current player index is set to the player that moves next


class GameRunner(object):
    def __init__(self, game_engine, agent_objects, save=True, max_turns=None):
        self.game_engine = game_engine
        self.agent_ids, self.players = zip(*agent_objects)
        self.game_states = []
        self.save = save
        self.max_turns = max_turns

    def run_game(self):
        # self.game_engine.reset()
        state = self.game_engine.get_state()
        self.game_states.append({"game_state": state,
                                 "last_move": None,
                                 "player_ids": self.agent_ids
                                 })

        player_index = self.game_engine.get_current_player()

        turn_num = 0
        while not self.game_engine.game_over():
            # TODO: streamline public vs private information.

            last_player = player_index
            engine_state = self.game_engine.get_state(player_index)
            engine_state['current_player'] = player_index
            engine_state['last_player'] = last_player

            move = self.players[player_index].move(engine_state)

            self.game_engine.move(move)

            # get global state
            state = self.game_engine.get_state()

            # save and broadcast data
            data_to_save = {}
            data_to_save["game_state"] = copy.deepcopy(state)
            data_to_save["last_move"] = copy.deepcopy(move)
            data_to_save["player_ids"] = copy.deepcopy(self.agent_ids)
            data_to_save["game_state"]["game_over"] = str(self.game_engine.game_over())
            data_to_save["game_state"]['current_player'] = player_index
            data_to_save["game_state"]['last_player'] = last_player

            self.game_states.append(data_to_save)

            # broadcast to observers
            self.broadcast(data_to_save)

            # get next player
            player_index = self.game_engine.get_current_player()
            turn_num += 1
            if self.max_turns is not None and turn_num > self.max_turns:
                break

        # the final scores
        scores = self.game_engine.get_state()["scores"]
        # in case scores is a dict-like object: convert to list
        scores = [scores[i] for i in range(len(scores))]

        if self.save:
            # save game states and player stats to the DB.
            game_id = game_data.save_game_history(self.game_engine.get_game_name(),
                                                  self.game_states)
            for index, agent_id in enumerate(self.agent_ids):
                score = scores[index]
                agent_data.save_game_result(agent_id, game_id,
                                            self.game_engine.type,
                                            score,
                                            max(scores) == score,
                                            datetime.utcnow())

        return scores

    def broadcast(self, data):
        state = data["game_state"]
        for player in self.players:
            player.observe(state)
