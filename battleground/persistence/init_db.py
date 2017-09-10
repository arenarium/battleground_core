import game_data

db_handle = game_data.get_db_handle()
collection = db_handle["game_states"]
collection.create_index("game_id")
for index in collection.list_indexes():
    print(index)

collection = db_handle["games"]
collection.create_index("utc_time")
for index in collection.list_indexes():
    print(index)
