from ReversiBot import *
import UtilMoveValidness as UMV

class StaticBot(ReversiBot):

    def __init__(self, grid, depth, bColor, pColor):
        super().__init__(grid, depth, bColor, pColor)
        self.model = list();
        startList = [0, grid]
        self.buildMinimax(UMV.isDone(grid, pColor), startList, 0, pColor)

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
        for branch in self.model:
            v = (copy.copy(branch[2]), branch[0])
            bestGrid = self.min(bestGrid, v, player)
        self.trimModel(bestGrid[0], player)
        return bestGrid[0]

    def updateMinimax(self, player):
        tmp = list()
        for branch in self.model:
            if len(branch) == self.depth + 1:
                moves = UMV.isDone(branch[self.depth], player * pow(-1, self.depth))
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
            if branch[2] == grid:
                branch.pop(1)
                tmp.append(branch)
        self.model = tmp
        self.updateMinimax(player)
        pass