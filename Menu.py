import pygame as pg
from Reversi import *
from HumanPlayer import HumanPlayer
from HeuristicBot import HeuristicBot
from ReversiBot import ReversiBot


class Menu():
    screenwidth = 500
    # DEFINE COLORS
    background_color = (0, 128, 30)
    white = (255, 255, 255)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    yellow = (255, 255, 0)
    color_inactive = pg.Color('lightskyblue3')
    color_active = pg.Color('dodgerblue2')
    # COLOR VARIABLES
    size_color = color_active
    # BOXES
    # size_up_button
    # RETURINNG VALUES
    size = 8
    play = False

    playerNames = ["Reversi", "Alfa-Beta", "Human"]
    #HumanPlayer must be the last value
    playerClasses = [ReversiBot, HeuristicBot, HumanPlayer]
    player1_index = 0
    player2_index = 1
    player1 = playerNames[player1_index]
    player2 = playerNames[player2_index]

    player1_depth = 3
    player2_depth = 3
    player1_heuristic = (0.1, 0.2, 0.2, 0.5)
    player2_heuristic = (0.05, 0.05, 0.1, 2.9)

    def getSize(self):
        return int(self.size)

    def getPlay(self):
        return self.play

    def getPlayer1(self):
        return self.player1

    def getPlayer2(self):
        return self.player2

    def getPlayer1_depth(self):
        return self.player1_depth

    def getPlayer2_depth(self):
        return self.player2_depth

    def changePlayer1Name(self):
        self.player1_index = (self.player1_index + 1) % (len(self.playerNames) - 1)
        self.player1 = self.playerNames[self.player1_index]

    def changePlayer2Name(self):
        self.player2_index = (self.player2_index + 1) % len(self.playerNames)
        self.player2 = self.playerNames[self.player2_index]

    def initReversi(self):
        if self.player1 == self.playerNames[len(self.playerNames) - 1]:
            player1Class = HumanPlayer()
        else:
            player1Class = self.playerClasses[self.player1_index]
            player1Class = player1Class(self.player1_depth, self.player1_heuristic)

        if self.player2 == self.playerNames[len(self.playerNames )-1]:
            player2Class = HumanPlayer()
        else:
            player2Class = self.playerClasses[self.player2_index]
            player2Class = player2Class(self.player2_depth, self.player2_heuristic)

        return Reversi(self.size, player1Class, player2Class)




    def __init__(self):
        pg.init()
        clock = pg.time.Clock()
        self.screen = pg.display.set_mode((self.screenwidth, self.screenwidth))

        pg.display.set_caption("Menu")

        # FONTS
        self.largeFont2 = pg.font.SysFont("comicsansms", 72)
        self.font = pg.font.Font("./fonts/Roboto-Black.ttf", 26)
        self.littleFont = pg.font.Font("./fonts/Roboto-Black.ttf", 20)

        # TEXTS
        self.titleText = self.largeFont2.render("ReverSI", True, self.blue)
        self.sizeText = self.font.render("Size: ", True, self.green)

        pg.display.flip()
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    if size_up_button.collidepoint(event.pos):
                        if self.size < 98:
                            self.size += 2
                    if size_down_button.collidepoint(event.pos):
                        if self.size > 2:
                            self.size -= 2
                    if player1_button.collidepoint(event.pos):
                        self.changePlayer1Name()
                    if player2_button.collidepoint(event.pos):
                        self.changePlayer2Name()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        self.play = True
                        running = False

            self.screen.fill(self.background_color)
            # draw Reversi icons
            pg.draw.circle(self.screen, self.red, (45, 45), 20)
            pg.draw.circle(self.screen, self.blue, (100, 45), 20)
            pg.draw.circle(self.screen, self.blue, (45, 100), 20)
            pg.draw.circle(self.screen, self.red, (100, 100), 20)
            # draw ReverSI
            self.screen.blit(self.titleText, (self.screenwidth // 2 - self.titleText.get_width() // 2 + 50, 20))
            # draw "Size: "
            self.screen.blit(self.sizeText, (self.screenwidth // 2 - self.sizeText.get_width() // 2, 120))
            # draw size_box + size on it
            pg.draw.rect(self.screen, self.green,
                         pg.Rect(self.screenwidth // 2 + self.sizeText.get_width() // 2, 120, 40,
                                 self.sizeText.get_height()), 2)
            self.text = self.font.render(str(self.size), True, self.green)
            self.screen.blit(self.text, (self.screenwidth // 2 + self.sizeText.get_width() // 2 + 5, 120))
            # draw buttons for size
            xDistance = self.screenwidth // 2 + self.sizeText.get_width() + 20
            size_up_button = pg.Rect(xDistance, 120, 40, self.sizeText.get_height() // 2 - 1)
            size_down_button = pg.Rect(xDistance, 120 + self.sizeText.get_height() // 2 + 1, 40,
                                       self.sizeText.get_height() // 2 - 1)
            pg.draw.rect(self.screen, self.green, size_up_button)
            pg.draw.rect(self.screen, self.green, size_down_button)
            self.text = self.littleFont.render("+", True, self.red)
            self.screen.blit(self.text, (xDistance + self.text.get_width() + 3, 116))
            self.text = self.littleFont.render("-", True, self.red)
            self.screen.blit(self.text,
                             (xDistance + self.text.get_width() + 6, 114 + self.sizeText.get_height() // 2 + 1))
            # "VS" symbol
            self.text = self.largeFont2.render("VS", True, self.yellow)
            self.screen.blit(self.text, (
            self.screenwidth // 2 - self.text.get_width() // 2 + 8, 180 - self.text.get_height() // 2))
            # full tree vs alfa-beta
            player1_button = pg.Rect(self.screenwidth * 3 // 32, 160, 160, 40)
            pg.draw.rect(self.screen, self.green, player1_button)
            self.text = self.font.render(self.player1, True, self.red)
            self.screen.blit(self.text,
                             (player1_button.x + player1_button.width // 2 - self.text.get_width() // 2, 165))
            # draw options for player1
            player1_depth_box = pg.Rect(player1_button.x, player1_button.y + 50, 120, 40)
            pg.draw.rect(self.screen, self.green, player1_depth_box)
            self.text = self.font.render("Depth: " + str(self.player1_depth), True, self.red)
            self.screen.blit(self.text, (player1_depth_box.x + 5, player1_depth_box.y + 5))

            # TODO OPTIONS
            # DEPTH
            # 4 HEURISTICS
            # full tree vs alfa-beta vs player
            player2_button = pg.Rect(self.screenwidth // 8 * 5, 160, 160, 40)
            pg.draw.rect(self.screen, self.green, player2_button)
            self.text = self.font.render(self.player2, True, self.red)
            self.screen.blit(self.text,
                             (player2_button.x + player2_button.width // 2 - self.text.get_width() // 2, 165))
            # draw options for player2 IF NOT HUMAN
            if self.player2 != "Human":
                pass
                # TODO OPTIONS
                # DEPTH
                # 4 HEURISTICS

            # DEBUG INSTRUCTION
            self.text = self.font.render("Press space to play", True, self.red)
            self.screen.blit(self.text, (self.screenwidth // 2 - self.text.get_width() // 2, self.screenwidth - 100))

            # self.screen.blit(self.txt_surface, (self.size_input_box.x + 5, self.size_input_box.y + 5))
            # pg.draw.rect(self.screen, self.size_color, self.size_input_box, 2)

            pg.display.update()
