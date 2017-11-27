
from games.arena import arena_game
from games.arena import gladiator


class ArenaGameEngine(arena_game.ArenaGameEngine):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_move_options(self, gladiator_index):
        """
        Used by agent to get available moves
        :param gladiator_index: index in gladiators list
        :return: (dict) {name: {target: value}}
        """
        gladiator = self.gladiators[gladiator_index]
        options = super().get_move_options(gladiator_index=gladiator_index)

        # add options for "boost"
        targets = {}
        for attr, val in gladiator.boosts.items():
            values = list(range(-gladiator.get_boost_cost(attr=attr, val=val),
                                gladiator.cur_sp + 1))
            if len(values) > 0:
                targets[attr] = values
        if len(targets) > 0 and False:
            options["boost"] = targets

        return options

    def handle_event(self, event):
        if event.type is "boost":
            self.move_boost(event=event)
        else:
            super().handle_event(event=event)
        return None

    def move_boost(self, event):
        """
        Boosts target of owner of event by event value.
        :param event:
        :return: None
        """
        if isinstance(event.target, list):
            targets = event.target
        else:
            targets = [event.target]
        if isinstance(event.value, list):
            values = event.value
        else:
            values = [event.value]
        boosts = dict(zip(targets, values))
        self.gladiators[event.owner].set_boosts(boosts=boosts)
        return None


class Gladiator(gladiator.Gladiator):
    def __init__(self, cur_sp=None, boosts=None, *args, **kwargs):
        """
        :param cur_sp: current spirit points (if not full)
        :param boosts: dict of current boosts (if not none)
        """
        super().__init__(*args, **kwargs)
        self.max_sp = self.get_max_sp()
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
            for att, val in boosts.items():
                self.boosts[att] = val

    def get_init(self):
        init = super().get_init()
        init["cur_sp"] = self.cur_sp
        init["boosts"] = self.boosts
        return init

    def reset(self):
        super().reset()
        self.max_sp = self.get_max_sp()
        self.cur_sp = self.max_sp
        self.boosts = {"att": 0,
                       "eva": 0,
                       "dam": 0,
                       "prot": 0,
                       "speed": 0}
        return None

    def get_attack(self):
        """
        :return: melee + boost
        """
        att = super().get_attack() + self.boosts["att"]
        return att

    def get_evasion(self):
        """
        :return: eva + boost
        """
        eva = super().get_evasion() + self.boosts["eva"]
        return eva

    def get_damage(self):
        """
        returns list of [damage dice, damage sides]
        :return: [1 + boost, 2 + str]
        """
        [d_dice, d_side] = super().get_damage()
        d_dice = d_dice + self.boosts["dam"]
        return [d_dice, d_side]

    def get_protection(self):
        """
        returns list of [protection dice, protection sides]
        :return: [1 + boost, str]
        """
        [p_dice, p_side] = super().get_protection()
        p_dice = p_dice + self.boosts["prot"]
        return [p_dice, p_side]

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
        speed = super().get_speed() - self.boosts["speed"]
        return speed

    def get_boost_cost(self, attribute, value):
        """
        :param attribute:
        :param value:
        :return: (int) sp cost of boost of attribute by value
        """
        old_val = self.boosts[attribute]
        new_val = old_val + value
        cost = new_val * (new_val + 1) / 2 - old_val * (old_val + 1) / 2
        return int(cost)

    def set_boosts(self, boosts):
        """
        :param boosts: dict containing keys and values to boost;
                       boosting a key should reduce cur_sp by that amount
        :return: None
        """
        for attr, val in boosts.items():
            # cost for boosting: (1, 2, 3, 4, 5, ...) -> (1, 3, 6, 10, 15, ...)
            cost = self.get_boost_cost(attribute=attr, value=val)
            if cost <= self.cur_sp:
                self.cur_sp -= cost
                self.boosts[attr] += val
        return None

    def get_cost(self, action, value, *args, **kwargs):
        """
        :param action: (str)
        :param target: NotImplemented
        :param value: (int)
        :return: (int) cost in turn counts of a given action, given its target and value.
        """
        if action == "boost":
            cost = value * self.get_speed()
        else:
            cost = super().get_cost(action=action, value=value,
                                    *args, **kwargs)
        return int(cost)
