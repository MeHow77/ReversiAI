#from Network import *
from time import time
import random
import pickle
import UtilMoveValidness as UMV
from Reversi import *

game = Reversi(8) #rozmiar planszy kwadratowej
clock = pygame.time.Clock()
done = False

#playersColor = {"redP": -1, "blueP": 1}
#curPlayer = playersColor["blueP"]
while not done:
    clock.tick(20)
    for event in pygame.event.get():
        if event.type == pygame.QUIT or game.isDone():
            done = True
        game.eventController(event.type)


