import importlib
import inspect


def base_factory(cls_name, mod_modules):
    mod_list = []
    for module in mod_modules:
        for name, obj in inspect.getmembers(module):
            if name is cls_name and inspect.isclass(obj):
                mod_list.append(obj)
    # add base classes to mod_list
    if cls_name is "Dungeon":
        module = importlib.import_module("games.arena.dungeon")
        for name, obj in inspect.getmembers(module):
            if name is cls_name and inspect.isclass(obj):
                mod_list.append(obj)
    elif cls_name is "Event":
        module = importlib.import_module("games.arena.event")
        for name, obj in inspect.getmembers(module):
            if name is cls_name and inspect.isclass(obj):
                mod_list.append(obj)
    elif cls_name is "Gladiator":
        module = importlib.import_module("games.arena.gladiator")
        for name, obj in inspect.getmembers(module):
            if name is cls_name and inspect.isclass(obj):
                mod_list.append(obj)
    elif cls_name is "ArenaGameEngine":
        module = importlib.import_module("games.arena.arena_game")
        for name, obj in inspect.getmembers(module):
            if name is cls_name and inspect.isclass(obj):
                mod_list.append(obj)

    base_list = tuple(mod_list)
    return base_list


def modded_class_factory(engine_class, mod_paths=None):
    # if not mod_paths or mod_paths is None:
    #     return engine_class
    mod_modules = []
    for mod_path in mod_paths:
        mod_module = importlib.import_module(mod_path)
        mod_modules.append(mod_module)

    Dungeon = type("Dungeon", base_factory("Dungeon", mod_modules), {})
    Event = type("Event", base_factory("Event", mod_modules), {})
    Gladiator = type("Gladiator", base_factory("Gladiator", mod_modules), {})
    ArenaGameEngine = type("ArenaGameEngine", base_factory("ArenaGameEngine", mod_modules), {})

    ArenaGameEngine.dungeon_class = Dungeon
    ArenaGameEngine.event_class = Event
    ArenaGameEngine.gladiator_class = Gladiator

    return ArenaGameEngine


#
# def modded_instance_factory(engine_instance, mods):
#     for mod in reversed(mods):
#         engine_instance = mod(engine_instance)
#
# mod -> mod -> mod -> mod -> instance
#
# class BaseMod(object):
#     def __init__(self, engine):
#         super().__init__()
#         self.engine = engine
#
# class EngineMod(BaseMod):
#     def get_move_options(self, index):
#         options = self.engine.get_move_options(index)
#         # magic
#         return options
