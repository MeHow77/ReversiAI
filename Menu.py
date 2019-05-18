import pygame as pg
from ReversiBot import ReversiBot
from HeuristicBot import HeuristicBot
import numpy as np


class Menu():
    screenwidth = 500
    #DEFINE COLORS
    background_color = (0, 128, 30)
    white = (255, 255, 255)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    yellow = (255, 255, 0)
    color_inactive = pg.Color('lightskyblue3')
    color_active = pg.Color('dodgerblue2')
    #COLOR VARIABLES
    size_color = color_active
    #RETURINNG VALUES
    size = '6'
    play = False

    def getSize(self):
        return int(self.size)

    def getPlay(self):
        return self.play

    def __init__(self):
        pg.init()
        clock = pg.time.Clock()
        self.screen = pg.display.set_mode((self.screenwidth, self.screenwidth))
        pg.display.set_caption("Menu")

        #FONTS
        self.largeFont2 = pg.font.SysFont("comicsansms", 72)
        self.font = pg.font.Font("./fonts/Roboto-Black.ttf", 26)

        #TEXTS
        self.titleText = self.largeFont2.render("ReverSI", True, self.blue)
        self.sizeText = self.font.render("Size: ", True, self.green)

        pg.display.flip()
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    if self.size_input_box.collidepoint(event.pos):
                        pass
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        self.play = True
                        running = False



            self.screen.fill(self.background_color)

            # draw Reversi icons
            pg.draw.circle(self.screen, self.red,(45, 45),20)
            pg.draw.circle(self.screen, self.blue,(100, 45),20)
            pg.draw.circle(self.screen, self.blue, (45, 100),20)
            pg.draw.circle(self.screen, self.red, (100, 100),20)
            #draw ReverSI
            self.screen.blit(self.titleText, (self.screenwidth // 2 - self.titleText.get_width() // 2 + 50, 20))
            #draw "Size: "
            self.screen.blit(self.sizeText, (self.screenwidth//2, 200))
            #draw 
            pg.draw.rect(self.screen, self.green, self.size_input_box)
            self.screen.blit(self.txt_surface, (self.size_input_box.x + 5, self.size_input_box.y + 5))
            pg.draw.rect(self.screen, self.size_color, self.size_input_box, 2)

            pg.display.update()
