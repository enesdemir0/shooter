import pygame

from soldier import Soldier

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Shooter")

player = Soldier(screen, 200, 200, 3)

run = True

while run:

    player.draw()

    for event in pygame.event.get():
        #quit game
        if event.type == pygame.QUIT:
            run = False

pygame.quit()
