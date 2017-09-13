from battleground.game_runner import GameRunner

from games.arena.arena_game import ArenaGameEngine
from games.arena.dungeon import Dungeon
from games.arena.gladiator import Gladiator
from games.arena.arena_agent import ArenaAgent

from collections import deque
import random


def test_engine():
    age = ArenaGameEngine(num_players=2, type="Arena_1")
    assert age.get_game_name() == "Arena_1"
    assert isinstance(age.gladiators, list)
    assert isinstance(age.dungeon, Dungeon)
    assert isinstance(age.event_queue, list)
    state = age.get_state()
    assert isinstance(state, dict)
    assert "gladiators" in state
    assert "dungeon" in state
    assert "queue" in state
    assert isinstance(age.get_current_player(), int)
    assert isinstance(age.within_bounds([0, 0]), bool)
    assert isinstance(age.get_move_names(gladiator=state["gladiators"][0]), list)
    assert isinstance(age.get_targets(gladiator=state["gladiators"][0]), dict)
    assert isinstance(age.get_values(gladiator=state["gladiators"][0]), dict)
    assert isinstance(age.game_over(), bool)


def test_dungeon():
    size = [[random.randint(1, 20), random.randint(21, 50)],
            [random.randint(1, 20), random.randint(21, 50)]]
    dun = Dungeon(size)
    assert dun.size == size
    # assert isinstance(dun.world, list)
    # assert len(dun.world) == size[0]


def test_gladiator():
    pos = [random.randint(1, 100), random.randint(1, 100)]
    glad = Gladiator(pos=pos)
    assert isinstance(glad.pos, list)
    assert isinstance(glad.name, str)
    assert isinstance(glad.get_init(), dict)
    assert isinstance(glad.get_stats(), dict)
    assert isinstance(glad.get_skills(), dict)
    assert isinstance(glad.get_attack(), int)
    assert isinstance(glad.get_evasion(), int)
    assert isinstance(glad.get_damage(), list)
    assert isinstance(glad.get_protection(), list)
    assert isinstance(glad.get_max_hp(), int)
    assert isinstance(glad.max_hp, int)
    assert isinstance(glad.cur_hp, int)
    assert isinstance(glad.get_max_sp(), int)
    assert isinstance(glad.max_sp, int)
    assert isinstance(glad.cur_sp, int)
    assert isinstance(glad.is_dead(), bool)
    assert 0 < glad.get_speed()
    assert isinstance(glad.boosts, dict)
    assert glad.set_boosts({"speed": random.randint(1, 3)}) is None
    assert glad.cur_sp < glad.max_sp
    assert glad.boosts["speed"] > 0
    assert glad.move([1, 0]) is None
    assert len(glad.pos) == 2
    assert all([isinstance(glad.get_cost(action, value), int)
                for action, value in {"stay": 0,
                                      "move": 0,
                                      "attack": 0,
                                      "boost": random.randint(1, 10)}.items()
                ])
    new_pos = [x + y for x, y in zip(pos, [1, 0])]
    stats = {"str": random.randint(1, 3),
             "dex": random.randint(1, 3),
             "con": random.randint(1, 3)}
    skills = {"melee": random.randint(1, 3),
              "eva": random.randint(1, 3),
              "speed": random.randint(1, 3)}
    name = "Maximus"
    team = random.randint(1, 10)
    vlad = Gladiator(pos=new_pos, stats=stats, skills=skills,
                     name=name, team=team, cur_hp=1, cur_sp=1)
    assert vlad.pos == new_pos
    assert vlad.name == name
    assert vlad.team == team
    assert vlad.base_stats == stats
    assert vlad.base_skills == skills
    assert vlad.cur_hp == 1
    assert vlad.cur_sp == 1
    assert isinstance(vlad.attack(glad), float)


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
