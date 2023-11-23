import pygame




class Soldier(pygame.sprite.Sprite):
    def __init__(self, screen,  x, y, scale):
        self.screen = screen
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load("../img/player/Idle/0.png")
        self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        self.rect = img.get_rect()
        self.rect.center = (x, y)

    def draw(self):
        self.screen.blit(self.image, self.rect)
