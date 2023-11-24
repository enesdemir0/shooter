import pygame


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)

        self.speed = 10
        self.image = pygame.image.load("./Code/img/icons/bullet.png")
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


