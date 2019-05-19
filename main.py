
from Menu import *


menu = Menu()
if menu.getPlay() == False:
    quit()
#depth = window.getDepth()
size = menu.getSize()

game = menu.initReversi()  # rozmiar planszy kwadratowej

done = False

while not done:
    #clock.tick(20)
    for event in pygame.event.get():
        if event.type == pygame.QUIT or game.Quit():
            done = True
        game.eventController(event.type)

