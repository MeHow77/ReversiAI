import copy
import numpy as np
import UtilMoveValidness as UMV


class ReversiBot():

    def __init__(self, grid, depth, bColor, pColor):
        self.depth = depth
        self.bColor = bColor
        self.pColor = pColor

    def makeMove(self, grid, color, allMoves):
        return self.minimax(grid, allMoves, 0, color)

    def minimax(self, grid, allMoves, depth, player):
        if depth == self.depth or len(allMoves) == 0:
            # always evaluate grid for bot, but use minimax for player or bot
            return grid, self.evaluate(grid, allMoves, self.bColor)

        opp = player * -1
        bestGrid = (grid, np.Inf * player)
        for move in allMoves:  # move is (grid, x, y)
            newMoves = UMV.isDone(move[0], opp)
            v = self.minimax(move[0], newMoves, depth + 1, opp)
            bestGrid = self.min(bestGrid, v, player)
        if depth == 0:
            return bestGrid[0]  # return placed coins
        else:
            return grid, bestGrid[1]

    # TODO Evaluation f: stability
    def min(self, grid1, grid2, player):
        if player == self.bColor:
            return grid1 if grid1[1] >= grid2[1] else grid2
        else:
            return grid1 if grid1[1] < grid2[1] else grid2


    def evaluate(self, grid, playersMove, player):
        return self.coinParity(grid) + self.mobility(grid, playersMove, player) + self.cornerValue(grid)

    def coinParity(self, grid):
        maxPlayerCoins = 0
        minPlayerCoins = 0
        size = len(grid)
        if size == 8:
            V = [[] for _ in range(8)]
            V[0] = [20, -3, 11, 8, 8, 11, -3, 20]
            V[1] = [-3, -7, -4, 1, 1, -4, -7, -3]
            V[2] = [11, -4, 2, 2, 2, 2, -4, 11]
            V[3] = [8, 1, 2, -3, -3, 2, 1, 8]
            V[4] = [8, 1, 2, -3, -3, 2, 1, 8]
            V[5] = [11, -4, 2, 2, 2, 2, -4, 11]
            V[6] = [-3, -7, -4, 1, 1, -4, -7, -3]
            V[7] = [20, -3, 11, 8, 8, 11, -3, 20]

            for i in range(size):
                for j in range(size):
                    if grid[i][j] == self.bColor:
                        maxPlayerCoins += V[i][j]
                    elif grid[i][j] == self.pColor:
                        minPlayerCoins += V[i][j]
        else:
            for i in range(size):
                for j in range(size):
                    if grid[i][j] == self.bColor:
                        maxPlayerCoins += 1
                    elif grid[i][j] == self.pColor:
                        minPlayerCoins += 1
        if maxPlayerCoins + minPlayerCoins != 0:
            return 100 * (maxPlayerCoins - minPlayerCoins) / (maxPlayerCoins + minPlayerCoins)
        else:
            return 0

    def mobility(self, grid, pMoves, player):
        # we assume bot is always an maximazing player
        #but pMoves and player parameters are for optimazing calculation
        #TODO Check whether corners are the only possible move?
        return 0.08*self.actualMobility(grid, pMoves, player) + 0.36*self.potentialMobility(grid) + 0.56*self.cornerValue(grid)

    def actualMobility(self, grid, pMoves, player):
        otherPlayerMovesNo = len(UMV.isDone(grid, player * -1))
        playerMovesNo = len(pMoves)
        if player == self.bColor:
            maxPlayerNo, minPlayerNo = playerMovesNo, otherPlayerMovesNo
        else:
            maxPlayerNo, minPlayerNo = otherPlayerMovesNo, playerMovesNo
        if maxPlayerNo + maxPlayerNo != 0:
            return 100 * (maxPlayerNo - minPlayerNo) / (maxPlayerNo + minPlayerNo)
        else:
            return 0

    def potentialMobility(self, grid):
        minPlayer = 0
        maxPlayer = 0
        size = len(grid)
        for i in range(size):
            for j in range(size):
                if grid[i][j] == UMV.emptyCell:
                    left = 0
                    right = 0
                    # check left and right cells for this cell
                    if i > 0:
                        left = grid[i - 1][j]
                    if i < size - 1:
                        right = grid[i + 1][j]
                    if left == self.pColor or right == self.pColor:
                        minPlayer += 1
                    if left == self.bColor or right == self.bColor:
                        maxPlayer += 1
        if maxPlayer + minPlayer == 0:
            return 0
        else:
            return 100 * (maxPlayer - minPlayer) / (maxPlayer + minPlayer)

    def cornerValue(self, grid):
        size = len(grid)
        corners = [grid[0][size-1], grid[0][size-1], grid[size-1][0], grid[size-1][size-1]]
        maxPlayer = 0
        minPlayer = 0
        for corner in corners:
            if corner == self.bColor: #maxPlayer
                maxPlayer += 1
            elif corner == self.pColor: #minPlayer
                minPlayer += 1

        if maxPlayer + minPlayer == 0:
            return 0
        else:
            return 100 * (maxPlayer - minPlayer) / (maxPlayer + minPlayer)

    def stability(self, grid):
        maxPlayer = 0
        minPlayer = 0
        size = len(grid)
        for i in range(size):
            for j in range(size):
                if grid[i][j] == self.bColor:
                    maxPlayer += self.calcStability(grid[i][j], self.bColor)
                elif grid[i][j] == self.pColor:
                    minPlayer += self.calcStability(grid[i][j], self.pColor)

    def calcStability(self, cell, player):
        return 0









