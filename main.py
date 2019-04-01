#from Network import *
from time import time
import random
import pickle
from Reversi import *

game = Reversi(8) #rozmiar planszy kwadratowej
clock = pygame.time.Clock()
done = False
kolor = 1
while not done:
    clock.tick(20)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONUP:
            if(game.press(pygame.mouse.get_pos(), kolor)):
                kolor *=-1
                #invoke bot here
        if event.type == pygame.MOUSEMOTION:
            game.showcursor(pygame.mouse.get_pos(), kolor)