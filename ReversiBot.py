import copy
import numpy as np
import UtilMoveValidness as UMV


class ReversiBot():

    def __init__(self, depth, bColor, pColor):
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

    def min(self, grid1, grid2, player):
        if player == self.bColor:
            return grid1 if grid1[1] >= grid2[1] else grid2
        else:
            return grid1 if grid1[1] < grid2[1] else grid2

    def evaluate(self, grid, playersMove, player):
        # we assume bot is always an maximazing player
        # but pMoves and player parameters are for optimazing calculation
        return self.coinParity(grid) + self.mobility(grid, playersMove,player) +\
               self.cornerValue(grid) + self.stability(grid)

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
        return self.actualMobility(grid, pMoves, player) + self.potentialMobility(grid)

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
            if corner == self.bColor:  # maxPlayer
                maxPlayer += 1
            elif corner == self.pColor:  # minPlayer
                minPlayer += 1

        if maxPlayer + minPlayer == 0:
            return 0
        else:
            return 100 * (maxPlayer - minPlayer) / (maxPlayer + minPlayer)

    def stability(self, grid):
        size = len(grid)
        minPlayer = [0]
        maxPlayer = [0]
        stablePcs = {}
        pcsNo = 0
        #performance "trick" for early game
        pausingFields = [(0, 0), (0, 1), (1, 0),
                          (0, size - 1), (0, size - 2), (1, size - 1),
                          (size-2, 0), (size - 1, size - 1), (1, size - 1),
                          (size - 1, size - 2), (size - 2, size - 1), (size - 1, size - 1)]
        startFlag = 0
        for field in pausingFields:
            if grid[field[0]][field[1]] != 0:
                startFlag = 1
                break
        if startFlag == 0:
            return 0

        corners = [(0, 0, (1, 0), (0, 1)), (size - 1, 0, (0, 1), (-1, 0)),
                   (0, size - 1, (0, -1), (1, 0)), (size - 1, size - 1, (-1, 0), (0, -1))]
        #check walls and save stable pieces for performance
        for corner in corners:
            if grid[corner[0]][corner[1]] != UMV.emptyCell:
                self.saveWall(corner, grid, corner[2], stablePcs)
                self.saveWall(corner, grid, corner[3], stablePcs)

        for i in range(size):
            for j in range(size):
                if grid[i][j] != UMV.emptyCell:
                    pcsNo += 1
                    if self.calcStability(grid, j, i, stablePcs, grid[i][j]):
                        self.inc(maxPlayer) if grid[i][j] == self.pColor else self.inc(minPlayer)
                    else:
                        self.dec(maxPlayer) if grid[i][j] == self.pColor else self.dec(minPlayer)

        return 100 * (maxPlayer[0] - minPlayer[0]) / pcsNo

    def saveWall(self, corner, grid, dir, stablePcs):
            x = corner[1]
            y = corner[0]
            corner_val = grid[corner[0]][corner[1]]
            for i in range(len(grid)):
                if grid[y][x] == corner_val:
                    index = str(y) + str(x)
                    if index not in stablePcs:
                        stablePcs[index] = corner_val
                    x += dir[1]
                    y += dir[0]
                else:
                    break

            x = corner[1]
            y = corner[0]
            fullWallFlag = 1
            for i in range(len(grid)):
                if grid[y][x] == UMV.emptyCell:
                    fullWallFlag = 0
                    break
                x += dir[1]
                y += dir[0]

            if fullWallFlag == 1:
                x = corner[1]
                y = corner[0]
                for i in range(len(grid)):
                    index = str(y) + str(x)
                    if index not in stablePcs:
                        stablePcs[index] = corner_val
                    x += dir[1]
                    y += dir[0]


    def calcStability(self, grid, x, y, stablePcs, prevColor):
        if str(y) + str(x) in stablePcs:
            return True
        size = len(grid)
        if UMV.fitsInBoard(size, x, y) is False:
            return True
        if grid[y][x] == UMV.emptyCell:
            return False
        if grid[y][x] != prevColor:
            return False

        stablePc = 1
        for dir in UMV.directions:
            dx = x
            dy = y
            while(True):
                dx += dir[1]
                dy += dir[0]
                if UMV.fitsInBoard(size, dx, dy) is False:
                    break
                if grid[dy][dx] == UMV.emptyCell:
                    stablePc = 0
                    if self.calcStability(grid, x - dir[0], y - dir[1], stablePcs, prevColor):
                        stablePc = 1
                    else:
                        break
            if stablePc == 0:
                return False
            else:
                stablePcs[str(y) + str(x)] = grid[y][x]
                return True

    def inc(self, val):
        val[0] = val[0] + 1

    def dec(self, val):
        val[0] = val[0] - 1