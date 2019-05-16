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
        # we assume bot is always an maximazing player
        # but pMoves and player parameters are for optimazing calculation
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
        corners = [grid[0][0], grid[0][7], grid[7][0], grid[7][7]]
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

    def stability(self, grid, oppMoves):
        # TODO to debug print stablePcs during game in console
        maxPlayer = [0]
        minPlayer = [0]
        size = len(grid)
        unstablePcs = {}
        stablePcs = {}
        fullRows = []
        pcsNo = 0

        # find full rows
        for i in range(size):
            for j in range(size):
                if grid[i][j] == UMV.emptyCell:
                    break
            fullRows.append(i)

        # one possible way to check unstablity
        # # is (y,x) stable?
        # for y in fullRows:
        #     for x in range(size):
        #         stabilityFlag = 1
        #         for dir in UMV.directions:
        #             # checking a row is unecessary
        #             if dir == (-1, 0) or dir == (1, 0):
        #                 continue
        #
        #             dx = x + dir[0]
        #             dy = y + dir[1]
        #             while UMV.fitsInBoard(size, dx, dy):
        #                 # if row isn't full but can't be flanked then still can be stable
                          # isFlankable was changed a little
        #                 if grid[dy][dx] == UMV.emptyCell and self.isFlankable(grid, x, y, size, dir):
        #                     stabilityFlag = 0
        #                     break
        #             if stabilityFlag == 0:
        #                 break
        #         if stabilityFlag == 1:
        #             stablePcs[str(y) + ',' + str(x)] = grid[y][x]

        # for each possible move save unique unstable piece with its owner
        # for move in oppMoves:
        #     for i in range(size):
        #         for j in range(size):
        #             if move[i][j] != grid[i][j]:
        #                 index = str(i) + ',' + str(j)
        #                 if index not in unstablePcs:
        #                     unstablePcs[index] = grid[i][j]

        #other possible way to check
        for i in range(size):
            for j in range(size):
                if grid[i][j] != UMV.emptyCell:
                    pcsNo += 1
                    index = str(i) + ',' + str(j)
                    if self.isFlankable(grid, j, i, size):
                        unstablePcs[index] = grid[i][j]
                    else:
                        stablePcs[index] = grid[i][j]

        for i in range(size):
            for j in range(size):
                index = str(i) + ',' + str(j)
                if grid[i][j] == self.bColor:
                    if index in stablePcs:
                        self.inc(maxPlayer) if grid[i][j] == self.bColor else self.dec(minPlayer)
                    elif index in unstablePcs:
                        maxPlayer -= 1

        return 100 * (maxPlayer - minPlayer) / pcsNo

    def isFlankable(self, grid, x, y, size):
        for dir in UMV.directions:
            dx_opp = x
            dy_opp = y
            while UMV.fitsInBoard(size, dx_opp, dy_opp):
                if grid[dy_opp][dx_opp] == grid[y][x] * -1 or grid[dy_opp][dx_opp] == UMV.emptyCell:
                    return True
                else:
                    dx_opp += dir[0]
                    dy_opp += dir[1]

    def inc(self, val):
        val[0] = val[0] + 1
    def dec(self, val):
        val[0] = val[0] - 1