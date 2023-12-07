import random

import pygame

from soldier import Soldier
from bullet import Bullet, Grenade, Explosion
from bullet import explosion_group


class Control:
    def __init__(self):
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = int(self.SCREEN_WIDTH * 0.8)
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Shooter")
        self.player = Soldier(self.screen, "player", 200, 200, 1.65, 5, 5)

        self.grenade = False
        self.grenade_thrown = False

        self.bullet_group = pygame.sprite.Group()
        self.grenade_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.item_box_group = pygame.sprite.Group()

        self.bullet_img = pygame.image.load("./Code/img/icons/bullet.png").convert_alpha()
        self.grenade_img = pygame.image.load("./Code/img/icons/grenade.png").convert_alpha()

        heal_box_img = pygame.image.load("./Code/img/icons/health_box.png").convert_alpha()
        ammo_box_img = pygame.image.load("./Code/img/icons/ammo_box.png").convert_alpha()
        grenade_box_img = pygame.image.load("./Code/img/icons/grenade_box.png").convert_alpha()

        self.item_boxes = {
            "Health": heal_box_img,
            "Ammo": ammo_box_img,
            "Grenade": grenade_box_img,
        }

        self.enemy = Soldier(self.screen, "enemy", 500, 300, 1.65, 2, 0)
        self.enemy_group.add(self.enemy)
        self.enemy1 = Soldier(self.screen, "enemy", 300, 300, 1.65, 2, 0)
        self.enemy_group.add(self.enemy1)
        self.font = pygame.font.SysFont("Futura", 30)

    def make_shoot(self, player, x_cor, y_cor, direction):
        if player.shoot and player.shoot_cooldown == 0 and player.ammo > 0:
            player.shoot_cooldown = 20
            bullet = Bullet(x_cor, y_cor, direction)
            self.bullet_group.add(bullet)
            player.ammo -= 1

    def ai(self, enemy):
        if not self.player.alive:
            enemy.idling = True
            enemy.update_action(0)
        if enemy.alive and self.player.alive:
            if not enemy.idling and random.randint(1, 200) == 1:
                enemy.idling = True
                enemy.update_action(0)
                enemy.idling_counter = 50

            if enemy.vision.colliderect(self.player.rect):
                enemy.update_action(0)
                enemy.shoot = True
                self.make_shoot(enemy, enemy.rect.centerx + (enemy.direction * 10), enemy.rect.centery, enemy.direction)
            else:
                if not enemy.idling:
                    if enemy.direction == 1:
                        enemy.moving_right = True
                    else:
                        enemy.moving_right = False
                    enemy.moving_left = not enemy.moving_right
                    enemy.move()

                    enemy.move_counter += 1
                    enemy.vision.center = (enemy.rect.centerx + 95 * enemy.direction, enemy.rect.centery)
                    pygame.draw.rect(self.screen, (255, 0, 0), enemy.vision)
                    enemy.update_action(1)
                    if enemy.move_counter > 80:
                        enemy.direction *= -1
                        enemy.move_counter *= -1
                else:
                    enemy.idling_counter -= 1
                    if enemy.idling_counter == 0:
                        enemy.idling = False

    def create_grenade(self):
        return Grenade(self.player.rect.centerx + (self.player.direction * 50), self.player.rect.top,
                       self.player.direction)

    def draw_text(self, text, text_col, x, y):
        img = self.font.render(text, True, text_col)
        self.screen.blit(img, (x, y))

    def draw_health(self, x, y):
        health = self.player.health
        pygame.draw.rect(self.screen, (255, 255, 255), (x - 2, y - 2.5, (self.player.max_health * 5) + 103, 10), 1)

        for z in range(health):
            pygame.draw.rect(self.screen, (255, 0, 0), (x, y, 5, 5))
            x += 6

    def update(self):
        for enemy in self.enemy_group:
            self.ai(enemy)

            if enemy.shoot_cooldown != 0:
                enemy.shoot_cooldown -= 1

            enemy.update()
            enemy.check_alive()

        self.draw_text("AMMO:", (255, 255, 255), 10, 35)
        for x in range(self.player.ammo):
            self.screen.blit(self.bullet_img, (90 + (x * 10), 40))
        self.draw_text("GRENADES:", (255, 255, 255), 10, 60)
        for x in range(self.player.grenades):
            self.screen.blit(self.grenade_img, (140 + (x * 15), 60))
        self.draw_health(10, 10)

        self.player.update()
        explosion_group.draw(self.screen)
        explosion_group.update()

        self.item_box_group.draw(self.screen)
        self.item_box_group.update(player=self.player)

        self.grenade_group.draw(self.screen)
        self.grenade_group.update(self.player, self.enemy_group)

        self.player.check_alive()

        if self.player.shoot_cooldown != 0:
            self.player.shoot_cooldown -= 1

        # check collision with characters
        for enemy in self.enemy_group:
            self.bullet_group.update(enemy, self.bullet_group)

        self.bullet_group.update(self.player, self.bullet_group)

        self.bullet_group.draw(self.screen)
