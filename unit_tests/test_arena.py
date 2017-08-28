from battleground.game_runner import GameRunner

from games.arena.arena_game import ArenaGameEngine
from games.arena.dungeon import Dungeon
from games.arena.gladiator import Gladiator
from games.arena import arena_agent

from collections import deque
import random


def test_engine():
    age = ArenaGameEngine(num_players=2, type="Arena_1", size=[20, 20])
    assert age.get_game_name() == "Arena_1"
    assert isinstance(age.dungeon, Dungeon)
    assert isinstance(age.event_queue, deque)


def test_dungeon():
    size = [random.randint(1, 20), random.randint(1, 20)]
    dun = Dungeon(size)
    assert dun.size == size
    assert isinstance(dun.world, list)
    assert len(dun.world) == size[0]


def test_gladiator():
    pos = [random.randint(1, 100), random.randint(1, 100)]
    stats = {"str": random.randint(1, 10),
             "dex": random.randint(1, 10),
             "con": random.randint(1, 10)}
    skills = {"melee": random.randint(1, 10),
              "eva": random.randint(1, 10),
              "speed": random.randint(1, 10)}
    glad = Gladiator(pos=pos, name="Maximus", stats=stats, skills=skills)
    assert glad.pos == pos
    assert glad.name == "Maximus"
    assert glad.base_stats == stats
    assert glad.base_skills == skills
    assert isinstance(glad.get_stats(), dict)
    assert isinstance(glad.get_skills(), dict)
    assert isinstance(glad.get_attack(), int)
    assert isinstance(glad.get_evasion(), int)
    assert isinstance(glad.get_damage(), list)
    assert isinstance(glad.get_protection(), list)
    assert isinstance(glad.get_max_hp(), int)
    assert isinstance(glad.max_hp, int)
    assert isinstance(glad.cur_hp, int)
    assert 0 < glad.get_speed()


def test_player():
    assert True


def test_game():
    assert True


if __name__ == "__main__":
    test_engine()
    test_dungeon()
    test_gladiator()
    test_player()
    test_game()
