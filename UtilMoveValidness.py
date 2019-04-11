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
        dx = x + dir[0]
        dy = y + dir[1]
        if fitsInBoard(size, dx, dy):
            while (True):
                if copiedGrid[dx][dy] + player == 0:
                    # print("different-color stone")
                    dx += dir[0]
                    dy += dir[1]
                    if not fitsInBoard(size, dx, dy):
                        break
                    if copiedGrid[dx][dy] == player:
                        # print("ended by same-color stone")
                        result = True
                        flipCells((x, y), (dx, dy), dir, copiedGrid, player)
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

def flipCells(pPos, endPos, dir, grid, pColor):
    if dir[0] == 0:
        cellsToFlip = abs(pPos[1] - endPos[1]) - 1
    else:
        cellsToFlip = abs(pPos[0] - endPos[0]) - 1
    x = pPos[0]
    y = pPos[1]
    for i in range(cellsToFlip):
        x += dir[0]
        y += dir[1]
        grid[x][y] = pColor

def countCells(grid):
    cellsNo = 0
    for i in range(grid.shape[0]):
        cellsNo+=sum(grid[i])

    return cellsNo