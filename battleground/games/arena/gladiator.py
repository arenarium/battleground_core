import copy
import random
import math


class Gladiator(object):

    base_damage = 5  # + a compounding 25% bonus per point of str
    base_protection = 0  # + log2(1 + str)
                         # + a compounding 25% bonus per point of str
    base_speed = 12  # / (1 + 2/30 * speed + a compounding 33% bonus per point of dex )
    base_max_hp = 20  # + a compounding 20% bonus per point of con

    def __init__(self,
                 stats=None, skills=None, name="Nameless", team=1, cur_hp=None,
                 *args, **kwargs):
        """
        :param stats: dict {"str": int, "dex": int, "con": int}
        :param skills: dict {"melee": int, "eva": int, "speed": int}
        :param name: str
        :param team: int
        :param cur_hp: current hit points (if not full)
        """
        if stats is None:
            self.base_stats = {"str": 0,
                               "dex": 0,
                               "con": 0}
        else:
            self.base_stats = stats
        if skills is None:
            self.base_skills = {"melee": 0,
                                "eva": 0,
                                "speed": 0}
        else:
            self.base_skills = skills
        self.damage = self.base_damage
        self.protection = self.base_protection
        self.name = name
        self.team = team
        self.max_hp = self.get_max_hp()
        if cur_hp is None:
            self.cur_hp = self.max_hp
        else:
            self.cur_hp = cur_hp

    def get_init(self, *args, **kwargs):
        init = {"name": self.name,
                "team": self.team,
                "stats": self.base_stats,
                "skills": self.base_skills,
                # optional
                "cur_hp": self.cur_hp,
                }
        return init

    def reset(self):
        self.max_hp = self.get_max_hp()
        self.cur_hp = self.max_hp
        return None

    def get_stats(self):
        """
        :return: stats
        """
        return self.base_stats

    def get_skills(self):
        """
        :return: skills mod stats bonus
                 speed has a compounding dex bonus
        """
        cur_skills = copy.deepcopy(self.base_skills)
        stats = self.get_stats()
        cur_skills["melee"] += stats["str"]
        cur_skills["eva"] += stats["dex"]
        cur_skills["speed"] += stats["dex"]
        return cur_skills

    def get_attack(self):
        """
        :return: melee
        """
        skills = self.get_skills()
        att = skills["melee"]
        return att

    def get_evasion(self):
        """
        :return: eva
        """
        skills = self.get_skills()
        eva = skills["eva"]
        return eva

    def get_base_damage(self):
        return self.damage

    def get_damage(self):
        """
        :return: base damage + a compounding 25% bonus per point of str
                 (5, 6, 7, 9, 12, 15, ...)
        """
        stats = self.get_stats()
        damage = self.get_base_damage() * (1.25 ** stats["str"])
        return int(damage)

    def get_base_protection(self):
        return self.protection

    def get_protection(self):
        """
        :return: (base protection + log2(1 + str)) + a compounding 25% bonus per point of str
                 (0, 1, 2, 3, 5, 7, ...)
        """
        stats = self.get_stats()
        protection = (self.get_base_protection()
                      + math.log2(1 + max(0, stats["str"]))) * (1.25 ** stats["str"])
        return int(protection)

    def get_max_hp(self):
        """
        :return: 20 + a compounding 20% bonus per point of con
                 (20, 24, 28, 34, 41, 49, ...)
        """
        stats = self.get_stats()
        mhp = int(self.base_max_hp * (1.2 ** stats["con"]))
        return mhp

    def get_base_speed(self):
        skills = self.get_skills()
        return skills["speed"]

    def get_speed(self):
        """
        :return: 12 / (1 + 2/30 * speed + a compounding 33% bonus per point of dex )
        """
        stats = self.get_stats()
        speed_divisor = 1 + 2/30 * self.get_base_speed() * (4/3 ** stats["dex"])
        speed = self.base_speed / speed_divisor
        return speed

    def get_initiative(self):
        return self.get_speed()

    def is_dead(self):
        return bool(self.cur_hp <= 0)

    def is_hit(self, attack):
        """
        :param attack: (int)
               probability to get hit depending on attack - evasion:
                ( -5 ,  -4 ,  -3 ,  -2 ,  -1 ,   0 ,   1 ,   2 ,   3 ,   4 ,   5 )
                (0.15, 0.21, 0.28, 0.36, 0.45, 0.55, 0.64, 0.72, 0.79, 0.85, 0.90)
        :return: (bool)
        """
        hit = attack - self.get_evasion() + random.randint(1, 10) - random.randint(1, 10)
        return bool(hit >= 0)

    def attack(self, target):
        """
        :param target: object that has an is_hit() and a get_protection() method
        :return: (int) damage
        """
        damage = 0
        protection = 0
        if target.is_hit(attack=self.get_attack()):
            damage = self.get_damage()
            protection = target.get_protection()
        return int(max(damage - protection, 0))

    def get_cost(self, action, target, value, *args, **kwargs):
        """
        :param action: (str)
        :param target: NotImplemented
        :param value: (int)
        :return: (int) cost in turn counts of a given action, given its target and value.
        """
        cost = 1
        if action == "stay":
            cost = value
        elif action == "attack":
            cost = 1
        cost *= self.get_speed()
        return int(cost)
