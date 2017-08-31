class Dungeon(object):
    def __init__(self, size):
        """
        :param size: [int, int] list of coordinates
        """
        self.size = size
        self.world = [[[] for _ in range(size[1])] for _ in range(size[0])]
