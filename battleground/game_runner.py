

class GameRunner(object):

    def __init__(self, game_engine, players):
        self.game_engine = game_engine
        self.players = players

    def run_game(self):
        self.game_engine.reset()
        state = self.game_engine.get_state()
        player_index = self.game_engine.get_current_player()

        while not self.game_engine.game_over():
            move = self.players[player_index].move(state)
            self.game_engine.move(move)
            state = self.game_engine.get_state()

            self.broadcast(state)
            player_index = self.game_engine.get_current_player()
        return self.game_engine.scores

    def broadcast(self,state):
        pass
