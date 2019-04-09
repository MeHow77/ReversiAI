from ReversiBot import *
import UtilMoveValidness as UMV
import numpy as np

class StaticBot():

    def __init__(self, grid, depth, bColor, pColor):
        self.grid = grid
        self.depth = depth
        self.bColor = bColor
        self.pColor = pColor
        self.model = list();
        self.whosNext = pow(-1, self.depth)
        startList = [0, grid]
        self.buildMinimax(UMV.isDone(grid, pColor), startList, 0, pColor)

    def makeMove(self, color, allMoves):
        self.grid = self.minimax(self.grid, allMoves, 0, color)
        return self.grid

    def min(self, bestGrid, v, player):
        return bestGrid if bestGrid[1] * player >= v[1] * player else v

    def buildMinimax(self, allMoves, nowlist, depth, player):
        if depth == self.depth or len(allMoves) == 0:
            self.model.append(nowlist)
            return None
        for move in allMoves: #move is (tuples, x, y)
            tmplist = copy.copy(nowlist)
            tmplist.append(move[0])
            tmplist[0] = UMV.countCells(move[0])
            playerTmp = player * -1
            newMoves = UMV.isDone(move[0], playerTmp)
            self.buildMinimax(newMoves, tmplist, depth + 1, playerTmp)

    def minimax(self, grid, allMoves, depth, player):
        bestGrid = (self.model[0][1], np.NINF * player)
        listofnextmoveworths = list()
        for branch in self.model:
            add = True
            for each in listofnextmoveworths:
                if np.array_equal(each[0], branch[2]):
                    each = (branch[2],(each[1] + branch[0])/2)
                    add = False
                    break;
            if add:
                listofnextmoveworths.append((branch[2], branch[0]))
        for val in listofnextmoveworths:
            v = (copy.copy(val[0]), val[1])
            bestGrid = self.min(bestGrid, v, player)
        self.trimModel(bestGrid[0], player)
        return bestGrid[0]

    def updateMinimax(self, player):
        tmp = list()
        for branch in self.model:
            if len(branch) == self.depth + 1:
                moves = UMV.isDone(branch[self.depth], player * self.whosNext)
                for move in moves:  # move is (tuples, x, y)
                    tmplist = copy.copy(branch)
                    tmplist.append(move[0])
                    tmplist[0] = UMV.countCells(move[0])
                    tmp.append(tmplist)
                if moves == []:
                    self.whosNext *= -1
                    moves = UMV.isDone(branch[self.depth], player * self.whosNext)
                    for move in moves:  # move is (tuples, x, y)
                        tmplist = copy.copy(branch)
                        tmplist.append(move[0])
                        tmplist[0] = UMV.countCells(move[0])
                        tmp.append(tmplist)
                    if moves == []:
                        tmp.append(branch)
            else:
                tmp.append(branch)
        self.model = tmp
        pass

    def trimModel(self, grid, player):
        print(player)
        tmp = list()
        for branch in self.model:
            if np.array_equal(grid, branch[2]):
                branch.pop(1)
                tmp.append(branch)
        self.model = tmp
        self.updateMinimax(player)
        pass