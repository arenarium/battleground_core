from .persistence import game_data

class GameRunner(object):

    def __init__(self, game_engine, players):
        self.game_engine = game_engine
        self.players = players
        self.game_states= []
        self.game_moves =[]

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
            self.game_states.append(state)
            self.broadcast(state)

            player_index = self.game_engine.get_current_player()

        player_ids = [p.get_name() for p in self.players]
        game_data.save_game_history(game_engine.get_game_name(),player_ids,self.states)

        return self.game_engine.scores

    def broadcast(self,state):
        pass
