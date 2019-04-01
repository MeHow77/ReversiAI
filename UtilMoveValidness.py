from abc import ABCMeta


class UtilMoveValidness:
    __metaclass__ = ABCMeta


    @staticmethod
    def fitsInBoard(grid, x, y):
        return (len(grid) > x >= 0
                and len(grid) > y >= 0)

    @staticmethod
    def checkRules(grid, x, y):
        directions = [(-1, 0), (-1, 1), (-1, -1), (0, -1),
                      (0, 1), (1, 0), (1, -1), (1, 1)]  # listy kierunkowe są fajne

        fitsinboard = lambda x, y: (len(grid) > x >= 0
                                    and len(grid) > y >= 0)
        changingstones = list()
        result = False
        for dir in directions:
            tmplist = list()
            dx = dir[0]
            dy = dir[1]
            if fitsinboard(x + dx, y + dy):
                while (True):
                    if grid[x + dx][y + dy] + grid[x][y] == 0:
                        # print("different-color stone")
                        tmplist.append((x + dx, y + dy))
                        dx += dir[0]
                        dy += dir[1]
                        if not fitsinboard(x + dx, y + dy):
                            break
                        if grid[x + dx][y + dy] == grid[x][y]:
                            # print("ended by same-color stone")
                            result = True
                            changingstones.extend(tmplist)
                            break
                        continue
                    if grid[x + dx][y + dy] == 0:
                        # print("no neighbor")
                        break
                    if grid[x + dx][y + dy] == grid[x][y]:
                        # print("same-color neighbor")
                        break
        return result, changingstones

