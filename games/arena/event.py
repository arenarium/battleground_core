class Event(object):

    def __init__(self, owner, time_stamp, type, origin=None, target=None, value=None):
        """
        :param owner: (Gladiator)
        :param time_stamp: (float)
        :param type: (str) name of type of event
        :param origin: [int, int] position
        :param target: Gladiator OR [int, int] position OR (str) attribute to boost
        """
        self.owner = owner
        self.time_stamp = time_stamp
        self.type = type
        self.origin = origin
        self.target = target
        self.value = value
