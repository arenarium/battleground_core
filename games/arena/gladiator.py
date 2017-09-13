import copy
import random

from games.arena.calc import *


class Gladiator(object):

    def __init__(self, pos,
                 stats=None, skills=None, name="Nameless", team=1, cur_hp=None, cur_sp=None, boosts=None):
        """
        :param pos: [int, int]
        :param stats: dict {"str": int, "dex": int, "con": int}
        :param skills: dict {"melee": int, "eva": int, "speed": int}
        :param name: str
        :param team: int
        :param cur_hp: current hit points (if not full)
        :param cur_sp: current spirit points (if not full)
        :param boosts: dict of current boosts (if not none)
        """
        self.pos = pos
        if stats is None:
            self.base_stats = {"str": 0, "dex": 0, "con": 0}
        else:
            self.base_stats = stats
        if skills is None:
            self.base_skills = {"melee": 0, "eva": 0, "speed": 0}
        else:
            self.base_skills = skills
        self.name = name
        self.team = team
        self.range = 1
        self.max_hp = self.get_max_hp()
        self.max_sp = self.get_max_sp()
        if cur_hp is None:
            self.cur_hp = self.max_hp
        else:
            self.cur_hp = cur_hp
        if cur_sp is None:
            self.cur_sp = self.max_sp
        else:
            self.cur_sp = cur_sp
        self.boosts = {"att": 0,
                       "eva": 0,
                       "dam": 0,
                       "prot": 0,
                       "speed": 0}
        if boosts is not None:
            for att, val in boosts:
                self.boosts[att] = val

    def reset(self):
        self.max_hp = self.get_max_hp()
        self.cur_hp = self.max_hp
        self.max_sp = self.get_max_sp()
        self.cur_sp = self.max_sp
        self.boosts = {"att": 0,
                       "eva": 0,
                       "dam": 0,
                       "prot": 0,
                       "speed": 0}

    def get_init(self):
        init = {"pos": self.pos,
                "name": self.name,
                "team": self.team,
                "stats": self.base_stats,
                "skills": self.base_skills,
                # optional
                "cur_hp": self.cur_hp,
                "cur_sp": self.cur_sp,
                "boosts": self.boosts
                }
        return init

    def get_stats(self):
        """
        :return: stats
        """
        return self.base_stats

    def get_skills(self):
        """
        :return: skills mod stats bonus
        """
        cur_skills = copy.deepcopy(self.base_skills)
        stats = self.get_stats()
        cur_skills["melee"] += stats["str"]
        cur_skills["eva"] += stats["dex"]
        cur_skills["speed"] += stats["dex"]
        return cur_skills

    def get_attack(self):
        """
        :return: melee + boost
        """
        skills = self.get_skills()
        att = skills["melee"] + self.boosts["att"]
        return att

    def get_evasion(self):
        """
        :return: eva + boost
        """
        skills = self.get_skills()
        eva = skills["eva"] + self.boosts["eva"]
        return eva

    def get_damage(self):
        """
        returns list of [damage dice, damage sides]
        :return: [1 + boost, 2 + str]
        """
        stats = self.get_stats()
        d_dice = 1 + self.boosts["dam"]
        d_side = 2 + stats["str"]
        return [d_dice, d_side]

    def get_protection(self):
        """
        returns list of [protection dice, protection sides]
        :return: [1 + boost, str]
        """
        stats = self.get_stats()
        p_dice = 1 + self.boosts["prot"]
        p_side = 0 + stats["str"]
        return [p_dice, p_side]

    def get_max_hp(self):
        """
        :return: 20 + a compounding 20% bonus per point of con
                 (20, 24, 28, 34, 41, 49, ...)
        """
        stats = self.get_stats()
        mhp = int(20 * (1.2 ** stats["con"]))
        return mhp

    def get_max_sp(self):
        """
        :return: 10 + a compounding 10% bonus per point of con
                 (10, 11, 12, 13, 14, 16)
        """
        stats = self.get_stats()
        msp = int(10 * (1.1 ** stats["con"]))
        return msp

    def get_speed(self):
        """
        :return: 21 - speed - boost
        """
        skills = self.get_skills()
        speed = 21 - skills["speed"] - self.boosts["speed"]
        return speed

    def is_dead(self):
        return bool(self.cur_hp <= 0)

    def set_boosts(self, boosts):
        """
        :param boosts: dict containing keys and values to boost;
                       boosting a key should reduce cur_sp by that amount
        :return: None
        """
        for att, val in boosts.items():
            # cost for boosting: (1, 2, 3, 4, 5, ...) -> (1, 3, 6, 10, 15, ...)
            cost = val * (val + 1) / 2
            if cost <= self.cur_sp:
                self.cur_sp -= cost
                self.boosts[att] = val
        return None

    def attack(self, target):
        """
        :param target: object that has a position, evasion score and protection tuple
        :return: (int) damage
        """
        pos_o = self.pos
        pos_t = target.pos
        attack = self.get_attack()
        evasion = target.get_evasion()
        [d_dice, d_side] = self.get_damage()
        [p_dice, p_side] = target.get_protection()
        damage = 0
        protection = 0
        if dist(pos_o, pos_t) > self.range:
            return 0
        else:
            hit = attack - evasion  # + random.randint(1, 20) - random.randint(1, 20)
            if hit >= 0:
                damage = d_dice * (1 + d_side) / 2
                protection = p_dice * (1 + p_side) / 2
                # damage = sum([random.randint(1, d_side) for _ in range(d_dice)])
                # protection = sum([random.randint(1, p_side) for _ in range(p_dice)])
            return max(damage - protection, 0)

    def move(self, direction):
        """
        :param direction: [int, int] direction vector (list)
        :return: None
        """
        self.pos = [x + y for x, y in zip(self.pos, direction)]
        return None

    def get_cost(self, action, value):
        """
        :param action: (str)
        :param target: NotImplemented
        :param value: (int)
        :return: (int) cost in turn counts of a given action, given its target and value.
        """
        cost = 1
        if action == "stay":
            cost = value
        elif action == "move":
            cost = 1
        elif action == "attack":
            cost = 1
        elif action == "boost":
            cost = value
        cost *= self.get_speed()
        return cost
