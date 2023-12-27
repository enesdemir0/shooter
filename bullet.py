import pygame


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)

        self.speed = 10
        self.image = pygame.image.load("img/icons/bullet.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self, a, b):
        self.rect.x += (self.direction * self.speed)
        if self.rect.right < 0 or self.rect.left > 800:
            self.kill()
        if pygame.sprite.spritecollide(a, b, False):
            if a.alive:
                self.kill()
                a.health -= 20


explosion_group = pygame.sprite.Group()


class Grenade(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.timer = 100
        self.speed = 7
        self.vel_y = -11
        self.image = pygame.image.load("img/icons/grenade.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
        self.gravity = 0.75

        self.x = False

    def update(self, player, enemy_group):
        self.vel_y += self.gravity
        dx = self.direction * self.speed
        dy = self.vel_y

        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.speed = 0

        if self.rect.left + dx < 0 or self.rect.right + dx > 800:
            self.direction *= -1
            dx = self.direction * self.speed
        self.rect.x += dx
        self.rect.y += dy

        self.timer -= 1

        if self.timer <= 0:
            self.kill()
            explosion = Explosion(self.rect.x, self.rect.y, 0.5)
            explosion_group.add(explosion)
            if abs(self.rect.centerx - player.rect.centerx) < 80 and abs(self.rect.centery - player.rect.centery) < 80:
                player.health -= 50
            for enemy in enemy_group:
                if abs(self.rect.centerx - enemy.rect.centerx) < 80 and abs(
                        self.rect.centery - enemy.rect.centery) < 80:
                    enemy.health -= 50


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 6):
            img = pygame.image.load(f"img/explosion/exp{num}.png").convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            self.images.append(img)
        self.frame_index = 0
        self.image = self.images[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        Explosion_SPEED = 4
        self.counter += 1

        if self.counter >= Explosion_SPEED:
            self.counter = 0
            self.frame_index += 1
            if self.frame_index >= len(self.images):
                self.kill()
            else:
                self.image = self.images[self.frame_index]




class ItemBox(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y, item_boxes):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = item_boxes[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + 80 / 2, y + (80 - self.image.get_height()))

    def update(self, player):
        if pygame.sprite.collide_rect(self, player):
            # Check what kind of box it was
            if self.item_type == "Health":
                player.health += 25
                if player.health > player.max_health:
                    player.health = player.max_health
                self.kill()

            elif self.item_type == "Ammo":
                player.ammo += 20
                self.kill()

            elif self.item_type == "Grenade":
                player.grenades += 3
                self.kill()
