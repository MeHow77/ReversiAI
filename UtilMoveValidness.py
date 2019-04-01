import copy

directions = [(-1, 0), (-1, 1), (-1, -1), (0, -1),
              (0, 1), (1, 0), (1, -1), (1, 1)]  # listy kierunkowe są fajne

players = {"redP": -1, "blueP": 1}

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


