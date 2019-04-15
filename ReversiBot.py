import copy
import numpy as np
import UtilMoveValidness as UMV


class ReversiBot():

    def __init__(self, grid, depth, bColor, pColor):
        self.grid = grid
        self.depth = depth
        self.bColor = bColor
        self.pColor = pColor
        self.evaluatedGrids = {}

    def makeMove(self, color, allMoves):
        self.grid = self.minimax(self.grid, allMoves, 0, color)
        return self.grid

    def minimax(self, grid, allMoves, depth, player):
        # Check whether such a grid was evaluated before
        if self.wasGridEvaluated(grid) is False:
            self.saveGrid(grid)
        if depth == self.depth or len(allMoves) == 0:
            return grid,  self.getEvalVal(grid)

        opp = player * -1
        bestGrid = (grid, np.Inf * opp)
        for move in allMoves:  # move is (grid, x, y)
            newMoves = UMV.isDone(move[0], opp)
            v = self.minimax(move[0], newMoves, depth + 1, opp)
            bestGrid = self.min(bestGrid, v, opp)
        if depth == 0:
            return bestGrid[0]  # return placed coins
        else:
            return grid, bestGrid[1]

    # TODO Evaluation f: coin parity, mobility, corners captured, stability
    def min(self, grid1, grid2, player):
        if player == self.bColor:
            return grid1 if grid1[1] >= grid2[1] else grid2
        else:
            return grid1 if grid1[1] < grid2[1] else grid2
        # return bestGrid if self.countCells(bestGrid[0], player) <= self.countCells(v[0], player) else v

    def wasGridEvaluated(self, grid):
        return grid.tostring() in self.evaluatedGrids

    def saveGrid(self, grid):
        self.evaluatedGrids[grid.tostring()] = self.evaluate(grid)

    def getEvalVal(self, grid):
        return self.evaluatedGrids[grid.tostring()]

    def evaluate(self, grid):
        cellsNo = 0
        for i in range(grid.shape[0]):
            cellsNo += sum(grid[i])
        return cellsNo
