class Event(object):

    def __init__(self, owner, type, time_stamp=0, origin=None, target=None, value=None):
        """
        :param owner: (Gladiator)
        :param time_stamp: (float)
        :param type: (str) name of type of event
        :param origin: [int, int] position
        :param target: Gladiator OR [int, int] position OR (str) attribute to boost
        """
        self.owner = owner
        self.type = type
        self.time_stamp = time_stamp
        self.origin = origin
        self.target = target
        self.value = value

    def get_init(self):
        init = {"owner": self.owner,
                "type": self.type,
                # "time_stamp": self.time_stamp,
                # "origin": self.origin,
                "target": self.target,
                "value": self.value
                }
        return init
