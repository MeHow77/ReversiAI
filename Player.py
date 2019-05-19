class Player():
    def __init__(self):
        pass

    def setColors(self, ownColor, otherPColor):
        self.ownColor = ownColor
        self.enemyColor = otherPColor

    def getOwnColor(self):
        return self.ownColor

    def getEnemyColor(self):
        return self.enemyColor

    def makeMove(self, grid,  allMoves):
        pass