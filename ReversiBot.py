import copy
import numpy as np

import UtilMoveValidness as UMV


class ReversiBot():

    def __init__(self, grid, depth, bColor, pColor):
        self.grid = grid
        self.depth = depth
        self.bColor = bColor
        self.pColor = pColor

    def makeMove(self):
        grid = self.minimax(self.grid, self.depth, self.bColor)
        self.grid = grid[0]
        return self.grid

    def minimax(self, grid, depth, player):
        if depth == 0 or UMV.isDone(grid, player):
            return grid, self.countCells(grid, player)

        (grid, cellsNo) = (grid, np.NINF if player == self.bColor else np.Inf)
        bestGrid = (grid, cellsNo)

        for i in range(len(grid)):
            for j in range(len(grid)):
                if grid[i][j] == UMV.emptyCell:
                    result = UMV.checkRules(grid, i, j, player)
                    if result[0]:
                        newGrid = copy.deepcopy(grid)
                        newGrid[i][j] = player
                        playerTmp = self.bColor if player == self.pColor else self.pColor
                        v = self.minimax(newGrid, depth - 1, playerTmp)
                        bestGrid = self.min(bestGrid, v, player) if player == self.pColor \
                            else self.max(bestGrid, v, player)
        return bestGrid
        #TODO save a moved what caused the most beneficial changes, not whole grid; save best score

    def countCells(self, grid, player):
        cellsNo = 0
        for i in range(len(grid)):
            for j in range(len(grid)):
                if grid[i][j] == player:
                    cellsNo += 1
        return cellsNo

    def max(self, bestGrid, v, player):
        return bestGrid if bestGrid[1] >= v[1] else v

    def min(self, bestGrid, v, player):
        return bestGrid if bestGrid[1] <= v[1] else v
