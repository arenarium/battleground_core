import copy
import random

from games.arena.calc import calc


class Gladiator(object):

    def __init__(self, pos, name, team, stats, skills):
        """
        :param pos: [int, int]
        :param name: str
        :param team: int
        :param stats: dict {"str": int, "dex": int, "con": int}
        :param skills: dict {"melee": int, "eva": int, "speed": int}
        """
        self.pos = pos
        self.name = name
        self.team = team
        self.base_stats = stats
        self.base_skills = skills
        self.range = 1
        self.max_hp = self.get_max_hp()
        self.cur_hp = self.max_hp
        self.max_sp = self.get_max_sp()
        self.cur_sp = self.max_sp
        self.boosts = {"att": 0,
                       "eva": 0,
                       "dam": 0,
                       "prot": 0,
                       "speed": 0}
        # available actions: {action: 0 - not allowed OR 1 - allowed}
        self.actions = {"move": 1,
                        "attack": 1,
                        "boost": 1}

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
        dd = 1 + self.boosts["dam"]
        ds = 2 + stats["str"]
        return [dd, ds]

    def get_protection(self):
        """
        returns list of [protection dice, protection sides]
        :return: [1 + boost, str]
        """
        stats = self.get_stats()
        pd = 1 + self.boosts["prot"]
        ps = 0 + stats["str"]
        return [pd, ps]

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
        for k, v in boosts.items():
            # cost for boosting: (1, 2, 3, 4, 5, ...) -> (1, 3, 6, 10, 15, ...)
            cost = v * (v + 1) / 2
            if cost <= self.cur_sp:
                self.cur_sp -= cost
                self.boosts[k] = v
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
        [dd, ds] = self.get_damage()
        [pd, ps] = target.get_protection()
        damage = 0
        protection = 0
        if calc.dist(pos_o, pos_t) > self.range:
            return 0
        else:
            hit = attack + random.randint(1, 20) - evasion - random.randint(1, 20)
            if hit > 0:
                damage = sum([random.randint(1, ds) for _ in range(dd)])
                protection = sum([random.randint(1, ps) for _ in range(pd)])
            return max(damage - protection, 0)

    def move(self, direction):
        """
        :param direction: [int, int] direction vector (list)
        :return: None
        """
        self.pos += direction
        return None

    def get_cost(self, action, value):
        if action == "move":
            return self.get_speed()
        elif action == "attack":
            return self.get_speed()
        elif action == "boost":
            return value * self.get_speed()
        else:
            return 0
