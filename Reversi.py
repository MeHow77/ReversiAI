import pygame
import UtilMoveValidness as UMV
from ReversiBot import ReversiBot
from StaticBot import StaticBot
import numpy as np

class Reversi():
    screenwidth = 500

    def __init__(self, size):
        pygame.init()
        if (size % 2 == 1):
            size += 1  # reversi wymaga parzystej ilości pól
        self.size = size
        self.screen = pygame.display.set_mode((
            self.screenwidth, self.screenwidth))
        self.grid = np.zeros( (size, size) )
        index = int(size / 2)
        self.grid[index][index] = 1
        self.grid[index - 1][index - 1] = 1
        self.grid[index][index - 1] = -1
        self.grid[index - 1][index] = -1  # te cztery na środku
        self.drawboard()
        self.updatescreen()
        self.cursor = (0, 0)
        self.finished = False
        self.finishFlags = {UMV.players["redP"] : 0,
                            UMV.players["blueP"]: 0}
        self.curPlayer = UMV.players["blueP"]
        self.botsColor = self.curPlayer * -1
        self.depth = 4
        self.botPlayer = ReversiBot(self.grid, self.depth, self.botsColor, self.curPlayer)


    def getXYfromMousePos(self, pos):
        x = int(pos[0] / (self.screenwidth / self.size))
        y = int(pos[1] / (self.screenwidth / self.size))
        return (x, y)

    def drawstone(self, color, x, y):
        cellwidth = self.screenwidth / self.size
        stonewidth = int(cellwidth / 2)
        stonerad = int(stonewidth / 3) * 2
        pygame.draw.circle(self.screen,
                           color,
                           (int(x * cellwidth + stonewidth),
                            int(y * cellwidth + stonewidth)),
                           stonerad, stonerad)

    def drawcell(self, color, x, y):
        cellwidth = self.screenwidth / self.grid.shape[0]
        pygame.draw.rect(self.screen, color,
                         pygame.Rect(x * cellwidth, y * cellwidth,
                                     cellwidth, cellwidth))

    def drawboard(self):
        cells = 0
        for i in range(0, self.grid.shape[0]):
            for j in range(0, self.grid.shape[0]):
                self.drawcell((255 * cells, 255 * cells, 255 * cells), i, j)
                cells ^= 1
            cells ^= 1  # to żeby self.curPlayery pól były na przemian
        return None

    def updatescreen(self):
        for i in range(0, self.grid.shape[0]):
            for j in range(0, self.grid.shape[0]):
                if self.grid[i][j] == -1:
                    self.drawstone((255, 0, 0), i, j)
                if self.grid[i][j] == 1:
                    self.drawstone((0, 0, 255), i, j)
        pygame.display.flip()
        return None

    def press(self,x , y):
        if self.grid[x][y] == UMV.emptyCell:
            resultTuple = UMV.checkRules(self.grid, x, y, self.curPlayer)
            if (resultTuple[0]):
                self.grid = resultTuple[1]
                self.botPlayer.trimModel(self.grid, self.curPlayer)
                self.updatescreen()
                self.finishFlags[UMV.players["blueP"]] = 0 #player could move
                return True
            else:
                return False

    def showcursor(self, x, y):
        if (self.cursor != (x, y)) and\
                UMV.fitsInBoard(self.size, x, y)\
                and (self.grid[x][y] == 0):
            i = self.cursor[0]
            j = self.cursor[1]
            if self.grid[i][j] == UMV.emptyCell:
                self.drawcell((255 * ((i + j) % 2), 255 * ((i + j) % 2), 255 * ((i + j) % 2)), i, j)
            if self.curPlayer == UMV.players["redP"]:
                color = (255, 0, 0)
            else:
                color = (0, 0, 255)
            self.drawstone(color, x, y)
            self.cursor = (x, y)
            pygame.display.flip()

    def twoBotsGame(self):
        while not self.isGameFinished():
            self.useBot()
            self.updatescreen()

    def eventController(self, event):
        if not self.isGameFinished():
            if self.curPlayer == self.botsColor:
                self.useBot()
                self.updatescreen()
            else:
                self.playerMoves(event)

    def useBot(self):
        allMoves = UMV.isDone(self.grid, self.curPlayer)
        if len(allMoves) != 0:
            self.finishFlags[self.curPlayer] = 0
            self.grid = self.botPlayer.makeMove(self.curPlayer, allMoves)
            self.curPlayer *= -1  # change player
        else:
            self.finishFlags[self.curPlayer] = 1
            self.curPlayer *= -1  # change player

    def playerMoves(self, event):
        allMoves = UMV.isDone(self.grid, self.curPlayer)
        if len(allMoves) != 0:
            self.finishFlags[self.curPlayer] = 0
            (x, y) = self.getXYfromMousePos(pygame.mouse.get_pos())
            if event == pygame.MOUSEBUTTONUP:
                if (self.press(x, y)):
                    self.curPlayer *= -1  # change player
            if event == pygame.MOUSEMOTION:
                self.showcursor(x, y)
        else:
            self.finishFlags[self.curPlayer] = 1
            self.curPlayer *= -1  # change player

    def isGameFinished(self):
        if (self.finishFlags[UMV.players["blueP"]] == \
        self.finishFlags[UMV.players["redP"]] == \
        self.finishFlags[self.curPlayer] == 1):
            self.finished = True
        return self.finished

    def Quit(self):
        #if player wants to end, set true...
        if self.finished:
            count = UMV.countCells(self.grid)
            print("Game finished")
            if count < 0:
                print("Red wins")
            else:
                if count > 0:
                    print("Blue wins")
                else:
                    print("Game tied")
            return True
        return False