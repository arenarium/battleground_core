from battleground.persistence import game_data


def create_indices():
    db_handle = game_data.get_db_handle()
    _game_states = db_handle["game_states"]
    _game_states.create_index("game_id")
    for index in _game_states.list_indexes():
        print(index)

    _games = db_handle["games"]
    _games.create_index("utc_time")
    for index in _games.list_indexes():
        print(index)


if __name__ == '__main__':
    create_indices()
