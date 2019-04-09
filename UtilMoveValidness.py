import copy
import numpy as np

directions = [(-1, 0), (-1, 1), (-1, -1), (0, -1),
              (0, 1), (1, 0), (1, -1), (1, 1)]  # listy kierunkowe są fajne

players = {"redP": -1, "blueP": 1}
emptyCell = 0

def fitsInBoard(length, x, y):
    return (length > x >= 0 and length > y >= 0)

def checkRules(grid, x, y, player):
    copiedGrid = grid.copy()
    copiedGrid[x][y] = player
    size = grid.shape[0]
    result = False
    for dir in directions:
        tmplist = list()
        dx = x + dir[0]
        dy = y + dir[1]
        if fitsInBoard(size, dx, dy):
            while (True):
                if copiedGrid[dx][dy] + player == 0:
                    # print("different-color stone")
                    tmplist.append((dx, dy))
                    dx += dir[0]
                    dy += dir[1]
                    if not fitsInBoard(size, dx, dy):
                        break
                    if copiedGrid[dx][dy] == player:
                        # print("ended by same-color stone")
                        result = True
                        for (i, j) in tmplist:
                            copiedGrid[i][j] = player
                        break
                    continue
                if copiedGrid[dx][dy] == 0:
                    # print("no neighbor")
                    break
                if copiedGrid[dx][dy] == player:
                    # print("same-color neighbor")
                    break
    return result, copiedGrid

def isDone(grid, player):
    allMoves = list()
    size = grid.shape[0]
    for row in range(0, size):
        for col in range(0, size):
            if grid[row][col] == emptyCell:
                result = checkRules(grid, row, col, player)
                if result[0]:
                    allMoves.append((result[1], row, col))
    return allMoves

def countCells(grid):
    cellsNo = 0
    for i in range(grid.shape[0]):
        cellsNo+=sum(grid[i])
    return cellsNo