from games.arena import arena_game
from games.arena import dungeon
from games.arena import event
from games.arena import gladiator

from games.arena.mods import position
from games.arena.mods import boosts


def base_factory(cls, mds):
    base_list = []
    for mod in mds:
        if cls in dir(games.arena.mods.mod):
            base_list.append(mod.cls)
    base_list.append()
    return base_list


def class_factory(cls, mds):
    class cls(*base_factory(cls, mds)):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
    return cls


class_factory(ArenaGameEngine, [position, boosts])
class_factory(Dungeon, [position, boosts])
class_factory(Event, [position, boosts])
class_factory(Gladiator, [position, boosts])
