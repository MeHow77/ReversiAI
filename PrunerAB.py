from ReversiBot import ReversiBot
import numpy as np
import UtilMoveValidness as UMV


class PrunerAB(ReversiBot):
    def __init__(self, depth, weights):
        super().__init__(depth, weights)

    def makeMove(self, grid,  allMoves):
        return self.alphaBeta(grid, allMoves, 0, self.ownColor, np.NINF, np.PINF)

    def alphaBeta(self, grid, allMoves, depth, player, a, b):
        if depth == self.depth or len(allMoves) == 0:
            return grid, self.evaluate(grid, allMoves, self.ownColor)

        opp = player * -1
        #?
        bestGrid = (grid, np.NINF * self.ownColor * player)
        for move in allMoves:  # move is (grid, x, y)
            newMoves = UMV.isDone(move[0], opp)
            v = self.alphaBeta(move[0], newMoves, depth + 1, opp, a, b)
            bestGrid, a, b = self.chooseGrid(bestGrid, v, player, a, b)
            if a >= b:
                break
        if depth == 0:
            return bestGrid[0]
        else:
            return grid, bestGrid[1]

    def chooseGrid(self, grid1, grid2, player, a, b):
        if player == self.ownColor:
            retGrid = grid1 if grid1[1] >= grid2[1] else grid2
            a = max(grid1[1], grid2[1])
        else:
            retGrid = grid1 if grid1[1] < grid2[1] else grid2
            b = min(grid1[1], grid2[1])
        return retGrid, a, b
