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
        game.eventController(event.type)

