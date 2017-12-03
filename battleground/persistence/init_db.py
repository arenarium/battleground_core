from . import game_data

db_handle = game_data.get_db_handle()
game_states = db_handle["game_states"]
game_states.create_index("game_id")
for index in game_states.list_indexes():
    print(index)

games = db_handle["games"]
games.create_index("utc_time")
for index in games.list_indexes():
    print(index)
