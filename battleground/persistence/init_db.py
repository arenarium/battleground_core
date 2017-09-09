import game_data

db = game_data.get_db()
collection = db["game_states"]
collection.create_index("game_id")
for index in collection.list_indexes():
    print(index)

collection = db["games"]
collection.create_index("utc_time")
for index in collection.list_indexes():
    print(index)
