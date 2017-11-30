class Event(object):

    def __init__(self, owner, type, time_stamp=0, target=None, value=None, *args, **kwargs):
        """
        :param owner: (int) gladiator index
        :param time_stamp: (float)
        :param type: (str) name of type of event
        :param target: (int) Gladiator index
        """
        self.owner = owner
        self.type = type
        self.time_stamp = time_stamp
        self.target = target
        self.value = value

    def get_init(self):
        init = {"owner": self.owner,
                "type": self.type,
                "time_stamp": self.time_stamp,
                "target": self.target,
                "value": self.value
                }
        return init
