

class ReversiBot():
    import UtilMoveValidness as UMV

    def __init__(self, grid, depth):
        self.grid = grid
        self.depth = depth