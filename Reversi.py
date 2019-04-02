import pygame
import UtilMoveValidness as UMV
from ReversiBot import ReversiBot


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
        self.updatescreen()
        self.cursor = (0, 0)

        self.finishFlags = {UMV.players["redP"] : 0,
                            UMV.players["blueP"]: 0}

        self.curPlayer = UMV.players["blueP"]
        self.botsColor = self.curPlayer * -1

        depth = 4
        self.botPlayer = ReversiBot(self.grid, depth, self.botsColor, self.curPlayer)


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

    def updatescreen(self):
        for i in range(0, len(self.grid)):
            for j in range(0, len(self.grid)):
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
                self.grid[x][y] = self.curPlayer
                for (x1, y1) in resultTuple[1]:
                    self.grid[x1][y1] = self.curPlayer
                self.updatescreen()
                self.finishFlags[UMV.players["blueP"]] = 0 #player could move
                return True
            else:
                return False



    def showcursor(self, x, y):
        if (self.cursor != (x, y)) and\
                UMV.fitsInBoard(self.grid, x, y)\
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


    def eventController(self, event):
        if self.curPlayer == self.botsColor:
            self.useBot()
            self.updatescreen()
        else:
            self.playerMoves(event)
        if self.finishFlags[UMV.players["blueP"]] ==\
                self.finishFlags[UMV.players["redP"]] ==\
                self.finishFlags[self.curPlayer] == 1:
            print("Game finished")


    def useBot(self):
        self.finishFlags[self.botsColor] = 1
        if UMV.isDone(self.grid, self.botsColor)[0] == False:
            self.finishFlags[self.botsColor] = 0
            self.grid = self.botPlayer.makeMove()
            self.curPlayer *= -1  # change player
        else:
            self.curPlayer *= -1  # change player


    def playerMoves(self, event):
        self.finishFlags[self.curPlayer] = 1
        if UMV.isDone(self.grid, self.curPlayer)[0] == False:
            self.finishFlags[self.curPlayer] = 0
            (x, y) = self.getXYfromMousePos(pygame.mouse.get_pos())
            if event == pygame.MOUSEBUTTONUP:
                if (self.press(x, y)):
                    self.curPlayer *= -1  # change player
            if event == pygame.MOUSEMOTION:
                self.showcursor(x, y)
        else:
            self.curPlayer *= -1  # change player

    def Quit(self):
        #if player wants to end, set true...
        return False