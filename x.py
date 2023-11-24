import pygame

from soldier import Soldier
from bullet import Bullet




class Control:
    def __init__(self, ammo):
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = int(self.SCREEN_WIDTH * 0.8)
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Shooter")
        self.player = Soldier(self.screen, "player", 200, 200, 3, 5)
        self.shoot = False
        self.shoot_cooldown = 0
        self.bullet_group = pygame.sprite.Group()
        self.ammo = ammo
        self.start_ammo = ammo
        self.enemy = self.create_enemy()

    def create_enemy(self):
        return Soldier(self.screen, "enemy", 200, 200, 3, 5)

    def make_shoot(self, x_cor, y_cor, direction):
        if self.shoot and self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 20
            bullet = Bullet(x_cor, y_cor, direction)
            self.bullet_group.add(bullet)
            self.ammo -= 1

    def update(self):
        self.player.update()
        self.player.check_alive()

        self.enemy.update()
        self.enemy.check_alive()

        if self.shoot_cooldown != 0:
            self.shoot_cooldown -= 1
        # check collision with characters
        self.bullet_group.update(self.enemy, self.bullet_group)
        self.bullet_group.update(self.player, self.bullet_group)
        self.bullet_group.draw(self.screen)






