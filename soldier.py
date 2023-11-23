import pygame


class Soldier(pygame.sprite.Sprite):
    def __init__(self, screen, char_type,  x, y, scale, speed):
        self.char_type = char_type
        self.moving_left = False
        self.moving_right = False
        self.screen = screen
        self.speed = speed
        self.direction = 1
        self.flip = False
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load(f"./img/{char_type}/Idle/0.png")
        self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        self.rect = img.get_rect()
        self.rect.center = (x, y)

    def move(self):
        dx = 0
        dy = 0

        if self.moving_left:
            dx = self.speed * -1
            self.direction = -1
            self.flip = True

        if self.moving_right:
            dx = self.speed
            self.direction = 1
            self.flip = False

        self.rect.x += dx
        self.rect.y += dy

    def draw(self):
        self.screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
