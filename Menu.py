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
    #(coinParity, mobility, corners, stability
    player1_heuristic = [0.15, 0.2, 0.2, 0.5]
    player2_heuristic = [0.05, 0.05, 0.1, 2.9]

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
        self.player1_index = (self.player1_index + 1) % (len(self.playerNames))
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
        self.littleFont2 = pg.font.Font("./fonts/Roboto-Black.ttf", 16)


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
                        if self.size < 16:
                            self.size += 2
                    if size_down_button.collidepoint(event.pos):
                        if self.size > 2:
                            self.size -= 2
                    if player1_button.collidepoint(event.pos):
                        self.changePlayer1Name()
                    if player2_button.collidepoint(event.pos):
                        self.changePlayer2Name()
                    if player1_depth_up_button.collidepoint(event.pos):
                        if self.player1_depth < 9:
                            self.player1_depth += 1
                    if player1_depth_down_button.collidepoint(event.pos):
                        if self.player1_depth > 1:
                            self.player1_depth -= 1
                    if player1_coinParity_up_button.collidepoint(event.pos):
                        self.player1_heuristic[0] += 0.05
                        self.player1_heuristic[0] = float("{0:.2f}".format(self.player1_heuristic[0]))
                    if player1_coinParity_down_button.collidepoint(event.pos):
                        if self.player1_heuristic[0] > 0:
                            self.player1_heuristic[0] -= 0.05
                            self.player1_heuristic[0] = float("{0:.2f}".format(self.player1_heuristic[0]))
                    if player1_mobility_up_button.collidepoint(event.pos):
                        self.player1_heuristic[1] += 0.05
                        self.player1_heuristic[1] = float("{0:.2f}".format(self.player1_heuristic[1]))
                    if player1_mobility_down_button.collidepoint(event.pos):
                        if self.player1_heuristic[1] > 0:
                            self.player1_heuristic[1] -= 0.05
                            self.player1_heuristic[1] = float("{0:.2f}".format(self.player1_heuristic[1]))
                    if player1_cornerValue_up_button.collidepoint(event.pos):
                        self.player1_heuristic[2] += 0.05
                        self.player1_heuristic[2] = float("{0:.2f}".format(self.player1_heuristic[2]))
                    if player1_cornerValue_down_button.collidepoint(event.pos):
                        if self.player1_heuristic[2] > 0:
                            self.player1_heuristic[2] -= 0.05
                            self.player1_heuristic[2] = float("{0:.2f}".format(self.player1_heuristic[2]))
                    if player1_stability_up_button.collidepoint(event.pos):
                        self.player1_heuristic[3] += 0.05
                        self.player1_heuristic[3] = float("{0:.2f}".format(self.player1_heuristic[3]))
                    if player1_stability_down_button.collidepoint(event.pos):
                        if self.player1_heuristic[3] > 0:
                            self.player1_heuristic[3] -= 0.05
                            self.player1_heuristic[3] = float("{0:.2f}".format(self.player1_heuristic[3]))
                    if player2_depth_up_button.collidepoint(event.pos):
                        if self.player2_depth < 9:
                            self.player2_depth += 1
                    if player2_depth_down_button.collidepoint(event.pos):
                        if self.player2_depth > 1:
                            self.player2_depth -= 1
                    if player2_coinParity_up_button.collidepoint(event.pos):
                        self.player2_heuristic[0] += 0.05
                        self.player2_heuristic[0] = float("{0:.2f}".format(self.player2_heuristic[0]))
                    if player2_coinParity_down_button.collidepoint(event.pos):
                        if self.player2_heuristic[0] > 0:
                            self.player2_heuristic[0] -= 0.05
                            self.player2_heuristic[0] = float("{0:.2f}".format(self.player2_heuristic[0]))
                    if player2_mobility_up_button.collidepoint(event.pos):
                        self.player2_heuristic[1] += 0.05
                        self.player2_heuristic[1] = float("{0:.2f}".format(self.player2_heuristic[1]))
                    if player2_mobility_down_button.collidepoint(event.pos):
                        if self.player2_heuristic[1] > 0:
                            self.player2_heuristic[1] -= 0.05
                            self.player2_heuristic[1] = float("{0:.2f}".format(self.player2_heuristic[1]))
                    if player2_cornerValue_up_button.collidepoint(event.pos):
                        self.player2_heuristic[2] += 0.05
                        self.player2_heuristic[2] = float("{0:.2f}".format(self.player2_heuristic[2]))
                    if player2_cornerValue_down_button.collidepoint(event.pos):
                        if self.player2_heuristic[2] > 0:
                            self.player2_heuristic[2] -= 0.05
                            self.player2_heuristic[2] = float("{0:.2f}".format(self.player2_heuristic[2]))
                    if player2_stability_up_button.collidepoint(event.pos):
                        self.player2_heuristic[3] += 0.05
                        self.player2_heuristic[3] = float("{0:.2f}".format(self.player2_heuristic[3]))
                    if player2_stability_down_button.collidepoint(event.pos):
                        if self.player2_heuristic[3] > 0:
                            self.player2_heuristic[3] -= 0.05
                            self.player2_heuristic[3] = float("{0:.2f}".format(self.player2_heuristic[3]))
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
            if self.player1 != "Human":
                #DEPTH
                player1_depth_box = pg.Rect(player1_button.x, player1_button.y + 50, 110, 40)
                pg.draw.rect(self.screen, self.green, player1_depth_box)
                self.text = self.font.render("Depth: " + str(self.player1_depth), True, self.red)
                self.screen.blit(self.text, (player1_depth_box.x + 5, player1_depth_box.y + 5))

                player1_depth_up_button = pg.Rect(player1_depth_box.x + player1_depth_box.width + 5, player1_depth_box.y,45,18)
                pg.draw.rect(self.screen,self.green, player1_depth_up_button)
                self.text = self.littleFont.render("+1", True, self.red)
                self.screen.blit(self.text, (player1_depth_up_button.x + player1_depth_up_button.width//2 - self.text.get_width()//2, player1_depth_up_button.y - self.text.get_width()/8 ))


                player1_depth_down_button = pg.Rect(player1_depth_up_button.x,player1_depth_up_button.y + player1_depth_up_button.height + 4, player1_depth_up_button.width,player1_depth_up_button.height)
                pg.draw.rect(self.screen, self.green, player1_depth_down_button)
                self.text = self.littleFont.render("-1", True, self.red)
                self.screen.blit(self.text, (
                    player1_depth_down_button.x + player1_depth_down_button.width // 2 - self.text.get_width() // 2,
                    player1_depth_down_button.y - self.text.get_width() / 8))

                #COINPARITY
                player1_coinParity_box = pg.Rect(player1_depth_box.x,player1_depth_box.y+player1_depth_box.height+5,player1_depth_box.width,player1_depth_box.height)
                pg.draw.rect(self.screen, self.green, player1_coinParity_box)
                self.text = self.littleFont.render("coinP: " + str(self.player1_heuristic[0]), True, self.red)
                self.screen.blit(self.text, (player1_coinParity_box.x + 3, player1_coinParity_box.y + 10))

                player1_coinParity_up_button = pg.Rect(player1_depth_up_button.x,
                                                    player1_coinParity_box.y,
                                                    player1_depth_up_button.width, player1_depth_up_button.height)
                pg.draw.rect(self.screen, self.green, player1_coinParity_up_button)
                self.text = self.littleFont2.render("+0.05", True, self.red)
                self.screen.blit(self.text,
                                ((player1_coinParity_up_button.x + player1_coinParity_up_button.width//2 - self.text.get_width()//2, player1_coinParity_up_button.y)))

                player1_coinParity_down_button = pg.Rect(player1_coinParity_up_button.x,
                                                    player1_coinParity_up_button.y + player1_coinParity_up_button.height + 4,
                                                    player1_coinParity_up_button.width, player1_coinParity_up_button.height)
                pg.draw.rect(self.screen, self.green, player1_coinParity_down_button)
                self.text = self.littleFont2.render("-0.05", True, self.red)
                self.screen.blit(self.text, (
                    player1_coinParity_down_button.x + player1_coinParity_down_button.width // 2 - self.text.get_width() // 2,
                    player1_coinParity_down_button.y))

                #MOBILITY
                player1_mobility_box = pg.Rect(player1_depth_box.x,
                                                 player1_coinParity_box.y + player1_depth_box.height + 5,
                                                 player1_depth_box.width, player1_depth_box.height)
                pg.draw.rect(self.screen, self.green, player1_mobility_box)
                self.text = self.littleFont.render("mobil: " + str(self.player1_heuristic[1]), True, self.red)
                self.screen.blit(self.text, (player1_mobility_box.x + 3, player1_mobility_box.y + 10))

                player1_mobility_up_button = pg.Rect(player1_depth_up_button.x,
                                                       player1_mobility_box.y,
                                                       player1_depth_up_button.width, player1_depth_up_button.height)
                pg.draw.rect(self.screen, self.green, player1_mobility_up_button)
                self.text = self.littleFont2.render("+0.05", True, self.red)
                self.screen.blit(self.text,
                                 ((
                                 player1_mobility_up_button.x + player1_mobility_up_button.width // 2 - self.text.get_width() // 2,
                                 player1_mobility_up_button.y)))

                player1_mobility_down_button = pg.Rect(player1_mobility_up_button.x,
                                                         player1_mobility_up_button.y + player1_mobility_up_button.height + 4,
                                                         player1_mobility_up_button.width,
                                                         player1_mobility_up_button.height)
                pg.draw.rect(self.screen, self.green, player1_mobility_down_button)
                self.text = self.littleFont2.render("-0.05", True, self.red)
                self.screen.blit(self.text, (
                    player1_mobility_down_button.x + player1_mobility_down_button.width // 2 - self.text.get_width() // 2,
                    player1_mobility_down_button.y))

                #CORNERVALUE
                player1_cornerValue_box = pg.Rect(player1_depth_box.x,
                                               player1_mobility_box.y + player1_depth_box.height + 5,
                                               player1_depth_box.width, player1_depth_box.height)
                pg.draw.rect(self.screen, self.green, player1_cornerValue_box)
                self.text = self.littleFont.render("cornV:" + str(self.player1_heuristic[2]), True, self.red)
                self.screen.blit(self.text, (player1_cornerValue_box.x + 3, player1_cornerValue_box.y + 10))

                player1_cornerValue_up_button = pg.Rect(player1_depth_up_button.x,
                                                     player1_cornerValue_box.y,
                                                     player1_depth_up_button.width, player1_depth_up_button.height)
                pg.draw.rect(self.screen, self.green, player1_cornerValue_up_button)
                self.text = self.littleFont2.render("+0.05", True, self.red)
                self.screen.blit(self.text,
                                 ((
                                     player1_cornerValue_up_button.x + player1_cornerValue_up_button.width // 2 - self.text.get_width() // 2,
                                     player1_cornerValue_up_button.y)))

                player1_cornerValue_down_button = pg.Rect(player1_cornerValue_up_button.x,
                                                       player1_cornerValue_up_button.y + player1_cornerValue_up_button.height + 4,
                                                       player1_cornerValue_up_button.width,
                                                       player1_cornerValue_up_button.height)
                pg.draw.rect(self.screen, self.green, player1_cornerValue_down_button)
                self.text = self.littleFont2.render("-0.05", True, self.red)
                self.screen.blit(self.text, (
                    player1_cornerValue_down_button.x + player1_cornerValue_down_button.width // 2 - self.text.get_width() // 2,
                    player1_cornerValue_down_button.y))
                #STABILITY
                player1_stability_box = pg.Rect(player1_depth_box.x,
                                                  player1_cornerValue_box.y + player1_depth_box.height + 5,
                                                  player1_depth_box.width, player1_depth_box.height)
                pg.draw.rect(self.screen, self.green, player1_stability_box)
                self.text = self.littleFont.render("stabi:" + str(self.player1_heuristic[3]), True, self.red)
                self.screen.blit(self.text, (player1_stability_box.x + 3, player1_stability_box.y + 10))

                player1_stability_up_button = pg.Rect(player1_depth_up_button.x,
                                                        player1_stability_box.y,
                                                        player1_depth_up_button.width, player1_depth_up_button.height)
                pg.draw.rect(self.screen, self.green, player1_stability_up_button)
                self.text = self.littleFont2.render("+0.05", True, self.red)
                self.screen.blit(self.text,
                                 ((
                                     player1_stability_up_button.x + player1_stability_up_button.width // 2 - self.text.get_width() // 2,
                                     player1_stability_up_button.y)))

                player1_stability_down_button = pg.Rect(player1_stability_up_button.x,
                                                          player1_stability_up_button.y + player1_stability_up_button.height + 4,
                                                          player1_stability_up_button.width,
                                                          player1_stability_up_button.height)
                pg.draw.rect(self.screen, self.green, player1_stability_down_button)
                self.text = self.littleFont2.render("-0.05", True, self.red)
                self.screen.blit(self.text, (
                    player1_stability_down_button.x + player1_stability_down_button.width // 2 - self.text.get_width() // 2,
                    player1_stability_down_button.y))

            player2_button = pg.Rect(self.screenwidth // 8 * 5, 160, 160, 40)
            pg.draw.rect(self.screen, self.green, player2_button)
            self.text = self.font.render(self.player2, True, self.red)
            self.screen.blit(self.text,
                             (player2_button.x + player2_button.width // 2 - self.text.get_width() // 2, 165))
            # draw options for player2 IF NOT HUMAN
            if self.player2 != "Human":
                # DEPTH
                player2_depth_box = pg.Rect(player2_button.x, player2_button.y + 50, 110, 40)
                pg.draw.rect(self.screen, self.green, player2_depth_box)
                self.text = self.font.render("Depth: " + str(self.player2_depth), True, self.red)
                self.screen.blit(self.text, (player2_depth_box.x + 5, player2_depth_box.y + 5))

                player2_depth_up_button = pg.Rect(player2_depth_box.x + player2_depth_box.width + 5,
                                                  player2_depth_box.y, 45, 18)
                pg.draw.rect(self.screen, self.green, player2_depth_up_button)
                self.text = self.littleFont.render("+1", True, self.red)
                self.screen.blit(self.text, (
                player2_depth_up_button.x + player2_depth_up_button.width // 2 - self.text.get_width() // 2,
                player2_depth_up_button.y - self.text.get_width() / 8))

                player2_depth_down_button = pg.Rect(player2_depth_up_button.x,
                                                    player2_depth_up_button.y + player2_depth_up_button.height + 4,
                                                    player2_depth_up_button.width, player2_depth_up_button.height)
                pg.draw.rect(self.screen, self.green, player2_depth_down_button)
                self.text = self.littleFont.render("-1", True, self.red)
                self.screen.blit(self.text, (
                    player2_depth_down_button.x + player2_depth_down_button.width // 2 - self.text.get_width() // 2,
                    player2_depth_down_button.y - self.text.get_width() / 8))

                # COINPARITY
                player2_coinParity_box = pg.Rect(player2_depth_box.x,
                                                 player2_depth_box.y + player2_depth_box.height + 5,
                                                 player2_depth_box.width, player2_depth_box.height)
                pg.draw.rect(self.screen, self.green, player2_coinParity_box)
                self.text = self.littleFont.render("coinP: " + str(self.player2_heuristic[0]), True, self.red)
                self.screen.blit(self.text, (player2_coinParity_box.x + 3, player2_coinParity_box.y + 10))

                player2_coinParity_up_button = pg.Rect(player2_depth_up_button.x,
                                                       player2_coinParity_box.y,
                                                       player2_depth_up_button.width, player2_depth_up_button.height)
                pg.draw.rect(self.screen, self.green, player2_coinParity_up_button)
                self.text = self.littleFont2.render("+0.05", True, self.red)
                self.screen.blit(self.text,
                                 ((
                                 player2_coinParity_up_button.x + player2_coinParity_up_button.width // 2 - self.text.get_width() // 2,
                                 player2_coinParity_up_button.y)))

                player2_coinParity_down_button = pg.Rect(player2_coinParity_up_button.x,
                                                         player2_coinParity_up_button.y + player2_coinParity_up_button.height + 4,
                                                         player2_coinParity_up_button.width,
                                                         player2_coinParity_up_button.height)
                pg.draw.rect(self.screen, self.green, player2_coinParity_down_button)
                self.text = self.littleFont2.render("-0.05", True, self.red)
                self.screen.blit(self.text, (
                    player2_coinParity_down_button.x + player2_coinParity_down_button.width // 2 - self.text.get_width() // 2,
                    player2_coinParity_down_button.y))

                # MOBILITY
                player2_mobility_box = pg.Rect(player2_depth_box.x,
                                               player2_coinParity_box.y + player2_depth_box.height + 5,
                                               player2_depth_box.width, player2_depth_box.height)
                pg.draw.rect(self.screen, self.green, player2_mobility_box)
                self.text = self.littleFont.render("mobil: " + str(self.player2_heuristic[1]), True, self.red)
                self.screen.blit(self.text, (player2_mobility_box.x + 3, player2_mobility_box.y + 10))

                player2_mobility_up_button = pg.Rect(player2_depth_up_button.x,
                                                     player2_mobility_box.y,
                                                     player2_depth_up_button.width, player2_depth_up_button.height)
                pg.draw.rect(self.screen, self.green, player2_mobility_up_button)
                self.text = self.littleFont2.render("+0.05", True, self.red)
                self.screen.blit(self.text,
                                 ((
                                     player2_mobility_up_button.x + player2_mobility_up_button.width // 2 - self.text.get_width() // 2,
                                     player2_mobility_up_button.y)))

                player2_mobility_down_button = pg.Rect(player2_mobility_up_button.x,
                                                       player2_mobility_up_button.y + player2_mobility_up_button.height + 4,
                                                       player2_mobility_up_button.width,
                                                       player2_mobility_up_button.height)
                pg.draw.rect(self.screen, self.green, player2_mobility_down_button)
                self.text = self.littleFont2.render("-0.05", True, self.red)
                self.screen.blit(self.text, (
                    player2_mobility_down_button.x + player2_mobility_down_button.width // 2 - self.text.get_width() // 2,
                    player2_mobility_down_button.y))

                # CORNERVALUE
                player2_cornerValue_box = pg.Rect(player2_depth_box.x,
                                                  player2_mobility_box.y + player2_depth_box.height + 5,
                                                  player2_depth_box.width, player2_depth_box.height)
                pg.draw.rect(self.screen, self.green, player2_cornerValue_box)
                self.text = self.littleFont.render("cornV:" + str(self.player2_heuristic[2]), True, self.red)
                self.screen.blit(self.text, (player2_cornerValue_box.x + 3, player2_cornerValue_box.y + 10))

                player2_cornerValue_up_button = pg.Rect(player2_depth_up_button.x,
                                                        player2_cornerValue_box.y,
                                                        player2_depth_up_button.width, player2_depth_up_button.height)
                pg.draw.rect(self.screen, self.green, player2_cornerValue_up_button)
                self.text = self.littleFont2.render("+0.05", True, self.red)
                self.screen.blit(self.text,
                                 ((
                                     player2_cornerValue_up_button.x + player2_cornerValue_up_button.width // 2 - self.text.get_width() // 2,
                                     player2_cornerValue_up_button.y)))

                player2_cornerValue_down_button = pg.Rect(player2_cornerValue_up_button.x,
                                                          player2_cornerValue_up_button.y + player2_cornerValue_up_button.height + 4,
                                                          player2_cornerValue_up_button.width,
                                                          player2_cornerValue_up_button.height)
                pg.draw.rect(self.screen, self.green, player2_cornerValue_down_button)
                self.text = self.littleFont2.render("-0.05", True, self.red)
                self.screen.blit(self.text, (
                    player2_cornerValue_down_button.x + player2_cornerValue_down_button.width // 2 - self.text.get_width() // 2,
                    player2_cornerValue_down_button.y))
                # STABILITY
                player2_stability_box = pg.Rect(player2_depth_box.x,
                                                player2_cornerValue_box.y + player2_depth_box.height + 5,
                                                player2_depth_box.width, player2_depth_box.height)
                pg.draw.rect(self.screen, self.green, player2_stability_box)
                self.text = self.littleFont.render("stabi:" + str(self.player2_heuristic[3]), True, self.red)
                self.screen.blit(self.text, (player2_stability_box.x + 3, player2_stability_box.y + 10))

                player2_stability_up_button = pg.Rect(player2_depth_up_button.x,
                                                      player2_stability_box.y,
                                                      player2_depth_up_button.width, player2_depth_up_button.height)
                pg.draw.rect(self.screen, self.green, player2_stability_up_button)
                self.text = self.littleFont2.render("+0.05", True, self.red)
                self.screen.blit(self.text,
                                 ((
                                     player2_stability_up_button.x + player2_stability_up_button.width // 2 - self.text.get_width() // 2,
                                     player2_stability_up_button.y)))

                player2_stability_down_button = pg.Rect(player2_stability_up_button.x,
                                                        player2_stability_up_button.y + player2_stability_up_button.height + 4,
                                                        player2_stability_up_button.width,
                                                        player2_stability_up_button.height)
                pg.draw.rect(self.screen, self.green, player2_stability_down_button)
                self.text = self.littleFont2.render("-0.05", True, self.red)
                self.screen.blit(self.text, (
                    player2_stability_down_button.x + player2_stability_down_button.width // 2 - self.text.get_width() // 2,
                    player2_stability_down_button.y))

            # DEBUG INSTRUCTION
            self.text = self.font.render("Press space to play", True, self.yellow)
            self.screen.blit(self.text, (self.screenwidth // 2 - self.text.get_width() // 2, self.screenwidth - 60))

            pg.display.update()
