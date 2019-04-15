from ReversiBot import ReversiBot
import numpy as np
import UtilMoveValidness as UMV


class HeuristicBot(ReversiBot):
    def __init__(self, grid, depth, bColor, pColor):
        super().__init__(grid, depth, bColor, pColor)

    def makeMove(self, color, allMoves):
        return self.alphaBeta(self.grid, allMoves, 0, color, np.NINF, np.PINF)



    def alphaBeta(self, grid, allMoves, depth, player, a, b):
        if self.wasGridEvaluated(grid) is False:
            self.saveGrid(grid, allMoves, player)
        if depth == self.depth or len(allMoves) == 0:
            return grid, self.getEvaluation(grid)

        opp = player * -1

        if player == self.bColor:
            bestGrid = grid, np.NINF
            for move in allMoves:
                newMoves = UMV.isDone(grid, opp)
                otherGrid = self.alphaBeta(move[0], newMoves, depth + 1, opp, a, b)
                value = max(bestGrid[1], otherGrid[1])
                bestGrid, a = self.chooseGrid(bestGrid, otherGrid, player), max(a, value)
                if a >= b:
                    break
            if depth == 0:
                return bestGrid[0]  # return placed coins
            else:
                return grid, bestGrid[1]
        else:
            bestGrid = grid, np. PINF
            for move in allMoves:
                newMoves = UMV.isDone(grid, opp)
                otherGrid = self.alphaBeta(move[0], newMoves, depth + 1, opp, a, b)
                value = min(bestGrid[1], otherGrid[1])
                bestGrid, a = self.chooseGrid(bestGrid, otherGrid, player), min(b, value)
                if a >= b:
                    break
            if depth == 0:
                return bestGrid[0]  # return placed coins
            else:
                return grid, bestGrid[1]

    def chooseGrid(self, grid1, grid2, player):
        if player == self.bColor:
            return grid1 if grid1[1] >= grid2[1] else grid2
        else:
            return grid1 if grid1[1] < grid2[1] else grid2