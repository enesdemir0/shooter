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

run = True


def draw_bg():
    screen.fill((144, 201, 120))
    pygame.draw.line(screen, (255, 0, 0), (0, 300), (SCREEN_WIDTH, 300))


while run:

    clock.tick(FPS)
    draw_bg()
    player.update_animation()
    enemy.draw()
    enemy.update_animation()
    player.draw()
    player.move()

    if player.alive:

        if player.flay:
            player.update_action(2)
        elif player.moving_left or player.moving_right:
            player.update_action(1)
        else:
            player.update_action(0)

    for event in pygame.event.get():
        # quit game
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                player.moving_left = True
            if event.key == pygame.K_d:
                player.moving_right = True
            if event.key == pygame.K_w and player.alive and player.flay == False:
                player.jump = True
                player.flay = True

            if event.key == pygame.K_SPACE:
                run = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                player.moving_left = False

            if event.key == pygame.K_d:
                player.moving_right = False

    pygame.display.update()

pygame.quit()
