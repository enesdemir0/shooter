import pygame

from soldier import Soldier
from x import Control
from bullet import ItemBox

pygame.init()

clock = pygame.time.Clock()
FPS = 60

control = Control()

player = control.player

run = True

item_box = ItemBox("Health", 100, 220, control.item_boxes)
control.item_box_group.add(item_box)
item_box = ItemBox("Ammo", 400, 220, control.item_boxes)
control.item_box_group.add(item_box)
item_box = ItemBox("Grenade", 500, 220, control.item_boxes)
control.item_box_group.add(item_box)


def draw_bg():
    control.screen.fill((144, 201, 120))
    pygame.draw.line(control.screen, (255, 0, 0), (0, 300), (control.SCREEN_WIDTH, 300))


while run:
    clock.tick(FPS)
    draw_bg()

    control.update()

    if player.alive:
        control.make_shoot(player.rect.centerx + (player.direction * 50), player.rect.centery, player.direction)
        if control.grenade and not control.grenade_thrown and control.player.grenades > 0:
            grenade = control.create_grenade()
            control.grenade_group.add(grenade)
            control.player.grenades -= 1
            control.grenade_thrown = True

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
                control.shoot = True
            if event.key == pygame.K_r:
                control.grenade = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                player.moving_left = False
            if event.key == pygame.K_d:
                player.moving_right = False
            if event.key == pygame.K_SPACE:
                control.shoot = False
            if event.key == pygame.K_r:
                control.grenade = False
                control.grenade_thrown = False

    pygame.display.update()

pygame.quit()
