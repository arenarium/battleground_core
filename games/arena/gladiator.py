import copy


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
        self.max_hp = self.get_max_hp()
        self.cur_hp = self.max_hp
        self.max_sp = self.get_max_sp()
        self.cur_sp = self.max_sp
        self.boosts = {"att": 0,
                       "eva": 0,
                       "dam": 0,
                       "prot": 0,
                       "speed": 0}

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
        """
        stats = self.get_stats()
        mhp = int(20 * (1.2 ** stats["con"]))
        return mhp

    def get_max_sp(self):
        """
        :return: 10 + a compounding 10% bonus per point of con
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
        if self.cur_hp <= 0:
            return True
        else:
            return False

    def set_boosts(self, boosts):
        """
        :param boosts: dict containing keys and values to boost;
                       boosting a key should reduce cur_sp by that amount
        :return: None
        """
        for k, v in boosts.item():
            """ 
            # Introduce cost for boosting:
            if v < self.cur_sp:
                self.cur_sp -= v
            """
            self.boosts[k] = v
        return None

    def move(self, direction):
        """
        :param direction: [int, int] direction vector (list)
        :return: None
        """
        self.pos += direction
        return None
