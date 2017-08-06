from .persistence import game_data

class GameRunner(object):

    def __init__(self, game_engine, players,save=True):
        self.game_engine = game_engine
        self.players = list(players.values())
        self.player_ids = list(players.keys())
        self.game_states= []
        self.game_moves =[]
        self.save=save

    def run_game(self):
        self.game_engine.reset()
        state = self.game_engine.get_state()
        self.game_states.append(state)

        player_index = self.game_engine.get_current_player()

        while not self.game_engine.game_over():
            move = self.players[player_index].move(state)
            self.game_engine.move(move)
            self.game_moves.append(move)

            state = self.game_engine.get_state()
            state["last_move"]=move
            self.game_states.append(state)
            self.broadcast(state)

            player_index = self.game_engine.get_current_player()

        if self.save:
            game_data.save_game_history(self.game_engine.get_game_name(),
                                        self.player_ids,
                                        self.game_states)
        return self.game_engine.scores

    def broadcast(self,state):
        pass
