import pygame
import os


class Soldier(pygame.sprite.Sprite):
    def __init__(self, screen, char_type, x, y, scale, speed):
        self.alive = True
        self.char_type = char_type
        self.moving_left = False
        self.moving_right = False
        self.screen = screen
        self.speed = speed
        self.direction = 1
        self.jump = False
        self.vel_y = 0
        self.gravity = 0.75
        self.flip = False
        self.flay = False

        self.health = 100
        self.max_health = self.health

        self.animation_list = []
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        pygame.sprite.Sprite.__init__(self)
        temp_list = []

        animation_types = ["Idle", "Run", "Jump", "Death"]
        for animation in animation_types:
            temp_list = []
            num_of_frames = len(os.listdir(f"./Code/img/{char_type}/{animation}"))
            for i in range(num_of_frames):
                img = pygame.image.load(f"./Code/img/{char_type}/{animation}/{i}.png")
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.move()
        self.draw()
        self.update_animation()

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

        if self.jump:
            self.vel_y = -15
            self.jump = False

        # Gravity

        self.vel_y += self.gravity
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.flay = False

        self.rect.x += dx
        self.rect.y += dy

    def update_animation(self):
        ANIMATION_COOLDOWN = 120
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
                # self.animation_list[self.action][len(self.animation_list[self.action])]
            else:
                self.frame_index = 0

        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

    def update_action(self, new_action):
        if self.action != new_action:
            self.frame_index = 0
            self.action = new_action
            self.update_time = pygame.time.get_ticks()

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3)

    def draw(self):
        self.screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
