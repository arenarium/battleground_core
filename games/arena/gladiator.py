import copy


class Gladiator(object):

    def __init__(self, pos, name, stats, skills):
        """
        :param pos: [int, int]
        :param name: str
        :param stats: {"str": int, "dex": int, "con": int}
        :param skills: {"melee": int, "eva": int, "speed": int}
        """
        self.pos = pos
        self.name = name
        self.base_stats = stats
        self.base_skills = skills
        self.max_hp = self.get_max_hp()
        self.cur_hp = self.max_hp
        self.max_sp = self.get_max_sp()
        self.cur_sp = self.max_sp

    def get_stats(self):
        """
        :return: stats mod item / boost bonus
        """
        return self.base_stats

    def get_skills(self):
        """
        :return: skills mod stats / item bonus
        """
        cur_skills = copy.deepcopy(self.base_skills)
        stats = self.get_stats()
        cur_skills["melee"] += stats["str"]
        cur_skills["eva"] += stats["dex"]
        cur_skills["speed"] += stats["dex"]
        return cur_skills

    def get_attack(self):
        """
        :return: melee value
        """
        skills = self.get_skills()
        return skills["melee"]

    def get_evasion(self):
        """
        :return: dex value
        """
        skills = self.get_skills()
        return skills["eva"]

    def get_damage(self):
        """
        returns list of [damage dice, damage sides]
        :return: [1, 2 + str value]
        """
        stats = self.get_stats()
        dd = 1
        ds = 2
        if "str" in stats:
            ds += stats["str"]
        return [dd, ds]

    def get_protection(self):
        """
        returns list of [protection dice, protection sides]
        :return: [1, con]
        """
        stats = self.get_stats()
        pd = 1
        ps = 0
        if "con" in stats:
            ps += stats["con"]
        return [pd, ps]

    def get_max_hp(self):
        """
        :return: 20 + a compounding 20% bonus per point of con
        """
        stats = self.get_stats()
        mhp = 20
        if "con" in stats:
            mhp = int(20 * (1.2 ** stats["con"]))
        return mhp

    def get_max_sp(self):
        """
        :return: 10 + a compounding 10% bonus per point of con
        """
        stats = self.get_stats()
        msp = 10
        if "con" in stats:
            msp = int(10 * (1.1 ** stats["con"]))
        return msp

    def get_speed(self):
        """
        :return: 21 - speed value
        """
        skills = self.get_skills()
        speed = 21 - skills["speed"]
        return speed
