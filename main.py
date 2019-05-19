# from Network import *
from time import time
import random
import pickle
import UtilMoveValidness as UMV
from Reversi import *
from Menu import *


menu = Menu()
if menu.getPlay() == False:
    quit()
#depth = window.getDepth()
size = menu.getSize()
game = Reversi(size)  # rozmiar planszy kwadratowej

done = False

while not done:
    #clock.tick(20)
    for event in pygame.event.get():
        if event.type == pygame.QUIT or game.Quit():
            done = True
            break
        #game.twoBotsGame()
        game.eventController(event.type)

