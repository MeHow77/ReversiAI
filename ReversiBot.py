import copy
import numpy as np

import UtilMoveValidness as UMV


class ReversiBot():

    def __init__(self, grid, depth, bColor, pColor):
        self.grid = grid
        self.depth = depth
        self.bColor = bColor
        self.pColor = pColor

    def makeMove(self, color, allMoves):
        self.grid = self.minimax(self.grid, allMoves, 0, color)
        return self.grid

    def minimax(self, grid, allMoves, depth, player):
        if depth == self.depth or len(allMoves) == 0:
            return grid, UMV.countCells(grid)
        bestGrid = (grid, np.Inf * player)
        for move in allMoves: #move is (grid, x, y)
            playerTmp = player * -1
            newMoves = UMV.isDone(move[0], playerTmp)
            v = self.minimax(move[0], newMoves, depth + 1, playerTmp)
            bestGrid = self.min(bestGrid, v, playerTmp)
        if depth == 0:
            return bestGrid[0]
        else:
            return (grid, bestGrid[1])

    def min(self, bestGrid, v, player):
        return bestGrid if bestGrid[1]*player >= v[1]*player else v
        #return bestGrid if self.countCells(bestGrid[0], player) <= self.countCells(v[0], player) else v

    def trimModel(self, grid):
        pass