import copy
import numpy as np

import UtilMoveValidness as UMV


class ReversiBot():

    def __init__(self, grid, depth, bColor, pColor):
        self.grid = grid
        self.depth = depth
        self.bColor = bColor
        self.pColor = pColor

    def makeMove(self, color):
        grid = self.minimax(self.grid, 0, color)#self.bColor)
        self.grid = grid[0]
        return self.grid

    def minimax(self, grid, depth, player):
        allMoves =  UMV.isDone(grid, player)
        if depth == self.depth or allMoves[0]:
            return grid, UMV.countCells(grid, player)
        allMoves = allMoves[1]

        (grid, cellsNo) = (grid, np.NINF if player == self.bColor else np.Inf)
        bestGrid = (grid, cellsNo)

        for move in allMoves: #move is (tuples, x, y)
            newGrid = copy.deepcopy(grid)
            newGrid[move[1]][move[2]] = player
            for (x1, y1) in move[0]:
                newGrid[x1][y1] = player
            playerTmp = self.bColor if player == self.pColor else self.pColor
            v = self.minimax(newGrid, depth + 1, playerTmp)
            bestGrid = self.min(bestGrid, v, player) if player == self.pColor \
                else self.max(bestGrid, v, player)
        if depth == 0:
            return bestGrid
        else:
            return (grid, bestGrid[1])



    def max(self, bestGrid, v, player):
        return bestGrid if bestGrid[1] >= v[1] else v
        #return bestGrid if self.countCells(bestGrid[0], player) >= self.countCells(v[0], player) else v

    def min(self, bestGrid, v, player):
        return bestGrid if bestGrid[1] <= v[1] else v
        #return bestGrid if self.countCells(bestGrid[0], player) <= self.countCells(v[0], player) else v