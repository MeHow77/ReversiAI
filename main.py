# from Network import *
from time import time
import random
import pickle
import UtilMoveValidness as UMV
from Reversi import *

game = Reversi(8)  # rozmiar planszy kwadratowej
clock = pygame.time.Clock()
done = False

while not done:
    #clock.tick(20)
    for event in pygame.event.get():
        if event.type == pygame.QUIT or game.Quit():
            done = True
            break
        #game.twoBotsGame()
        game.eventController(event.type)
