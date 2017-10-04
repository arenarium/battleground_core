class Dungeon(object):
    def __init__(self, size):
        """
        :param size: [[int, int], [int, int]]
        """
        self.size = size
        # self.world = [[[] for _ in range(size[1])] for _ in range(size[0])]

    def get_init(self):
        init = {"size": self.size}
        return init

    def reset(self):
        pass

    def shrink_dungeon(self, state):
        # shrink dungeon
        positions = [g.pos for g in state["gladiators"]]
        pos_x = [p[0] for p in positions]
        pos_y = [p[1] for p in positions]
        self.size = ((min(pos_x), max(pos_x)), (min(pos_y), max(pos_y)))
        return None
