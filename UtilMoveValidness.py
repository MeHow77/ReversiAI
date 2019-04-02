import copy

directions = [(-1, 0), (-1, 1), (-1, -1), (0, -1),
              (0, 1), (1, 0), (1, -1), (1, 1)]  # listy kierunkowe są fajne

players = {"redP": -1, "blueP": 1}
emptyCell = 0

def fitsInBoard(grid, x, y):
    return (len(grid) > x >= 0
            and len(grid) > y >= 0)


def checkRules(grid, x, y, player):
    copiedGrid = copy.deepcopy(grid)
    copiedGrid[x][y] = player
    changingstones = list()
    result = False
    for dir in directions:
        tmplist = list()
        dx = dir[0]
        dy = dir[1]
        if fitsInBoard(copiedGrid, x + dx, y + dy):
            while (True):
                if copiedGrid[x + dx][y + dy] + copiedGrid[x][y] == 0:
                    # print("different-color stone")
                    tmplist.append((x + dx, y + dy))
                    dx += dir[0]
                    dy += dir[1]
                    if not fitsInBoard(copiedGrid, x + dx, y + dy):
                        break
                    if copiedGrid[x + dx][y + dy] == copiedGrid[x][y]:
                        # print("ended by same-color stone")
                        result = True
                        changingstones.extend(tmplist)
                        break
                    continue
                if copiedGrid[x + dx][y + dy] == 0:
                    # print("no neighbor")
                    break
                if copiedGrid[x + dx][y + dy] == copiedGrid[x][y]:
                    # print("same-color neighbor")
                    break
    return result, changingstones

def isDone(grid, player):
    allMoves = list()
    size = len(grid)
    done = True
    for row in range(size):
        for col in range(size):
            if grid[row][col] == emptyCell:
                result = checkRules(grid, row, col, player)
                if result[0]:
                    allMoves.append((result[1], row, col))
                    done = False
    return (done, allMoves)

def countCells(grid, player):
    cellsNo = 0
    for i in range(len(grid)):
        for j in range(len(grid)):
            if grid[i][j] == player:
                cellsNo += 1
    return cellsNo

