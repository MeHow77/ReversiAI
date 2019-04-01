import pygame
import math
import copy


import UtilMoveValidness as UMV


class Reversi():
    screenwidth = 500

    def __init__(self, size):
        pygame.init()
        self.screen = pygame.display.set_mode((
            self.screenwidth, self.screenwidth))
        if (size % 2 == 1):
            size += 1  # reversi wymaga parzystej ilości pól
        self.grid = list()
        for i in range(0, size):
            row = list()
            for j in range(0, size):
                row.append(0)  # puste pole(0) czerwone(-1) niebieskie(1)
            self.grid.append(row)
        index = int(size / 2)
        self.grid[index][index] = 1
        self.grid[index - 1][index - 1] = 1
        self.grid[index][index - 1] = -1
        self.grid[index - 1][index] = -1  # te cztery na środku
        self.drawboard()
        self.update()
        self.cursor = (0, 0)

        self.finishFlags = {UMV.players["redP"] : 0,
                            UMV.players["blueP"]: 0}

        self.curPlayer = UMV.players["blueP"]


    def getXYfromMousePos(self, pos):
        x = int(pos[0] / (self.screenwidth / len(self.grid)))
        y = int(pos[1] / (self.screenwidth / len(self.grid)))
        return (x, y)

    def drawstone(self, color, x, y):
        cellwidth = self.screenwidth / len(self.grid)
        stonewidth = int(cellwidth / 2)
        stonerad = int(stonewidth / 3) * 2
        pygame.draw.circle(self.screen,
                           color,
                           (int(x * cellwidth + stonewidth),
                            int(y * cellwidth + stonewidth)),
                           stonerad, stonerad)

    def drawcell(self, color, x, y):
        cellwidth = self.screenwidth / len(self.grid)
        pygame.draw.rect(self.screen, color,
                         pygame.Rect(x * cellwidth, y * cellwidth,
                                     cellwidth, cellwidth))

    def drawboard(self):
        cells = 0
        for i in range(0, len(self.grid)):
            for j in range(0, len(self.grid)):
                self.drawcell((255 * cells, 255 * cells, 255 * cells), i, j)
                cells ^= 1
            cells ^= 1  # to żeby self.curPlayery pól były na przemian
        return None

    def update(self):
        for i in range(0, len(self.grid)):
            for j in range(0, len(self.grid)):
                if self.grid[i][j] == -1:
                    self.drawstone((255, 0, 0), i, j)
                if self.grid[i][j] == 1:
                    self.drawstone((0, 0, 255), i, j)
        pygame.display.flip()
        return None

    def press(self, pos):
        (x, y) = self.getXYfromMousePos(pos)
        if self.grid[x][y] == 0:
            copiedGrid = self.grid.copy()
            resultTuple = UMV.checkRules(copiedGrid, x, y, self.curPlayer)
            if (resultTuple[0]):
                for (x1, y1) in resultTuple[1]:
                    self.grid[x1][y1] = self.curPlayer
                self.update()
                self.finishFlags[UMV.players["blueP"]] = 0 #player could move
                return True
            else:
                self.grid[x][y] = 0
                return False



    def showcursor(self, pos):
        (x, y) = self.getXYfromMousePos(pos)
        if (self.cursor != (x, y)) and\
                UMV.fitsInBoard(self.grid, x, y)\
                and (self.grid[x][y] == 0):
            i = self.cursor[0]
            j = self.cursor[1]
            if self.grid[i][j] == 0:
                self.drawcell((255 * ((i + j) % 2), 255 * ((i + j) % 2), 255 * ((i + j) % 2)), i, j)
            if self.curPlayer == UMV.players["redP"]:
                color = (255, 0, 0)
            else:
                color = (0, 0, 255)
            self.drawstone(color, x, y)
            self.cursor = (x, y)
            pygame.display.flip()


    def eventController(self, event):
        if event == pygame.MOUSEBUTTONUP:
            if(self.press(pygame.mouse.get_pos())):
                self.curPlayer *= -1 # change player
                #invoke bot here
        if event == pygame.MOUSEMOTION:
            self.showcursor(pygame.mouse.get_pos())


    #TODO store valid moves which will be used for: end detecting, player actions, bot's predicitons
    def isDone(self):
        size = len(self.grid)
        copiedGrid = self.grid.copy()

        for row in range(size):
            for col in range(size):
                if self.grid[row][col] == 0:
                    continue

                result = UMV.checkRules(copiedGrid, row, col, )

