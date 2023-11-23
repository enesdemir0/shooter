import pygame

from soldier import Soldier

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Shooter")

clock = pygame.time.Clock()
FPS = 60

player = Soldier(screen, "player", 200, 200, 3, 5)
enemy = Soldier(screen, "enemy", 400, 200, 3, 5)



print(player.moving_left)

run = True

while run:

    clock.tick(FPS)
    screen.fill((144, 201, 120))
    enemy.draw()
    player.draw()

    player.move()

    for event in pygame.event.get():
        # quit game
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                player.moving_left = True

            if event.key == pygame.K_d:
                player.moving_right = True
            if event.key == pygame.K_SPACE:
                run = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                player.moving_left = False
            if event.key == pygame.K_d:
                player.moving_right = False

    pygame.display.update()

pygame.quit()
