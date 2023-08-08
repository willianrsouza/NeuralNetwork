import pygame
from game.env import birds_images


class Bird:
    images = birds_images()
    max_rotation = 25
    rot_velocity = 20
    animation_time = 5

    def __init__(self, x=50, y=50):
        self.x = x
        self.y = y
        self.tilt = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.images[0]
        self.tick_count = 0

    def jump(self):
        self.vel = -8.0
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1

        down = self.vel * self.tick_count + 0.9 * self.tick_count ** 2

        if down >= 16:
            down = 13

        if down < 0:
            down -= 0.4

        self.y = self.y + down

        if down < 0 or self.y < self.height + 50:
            if self.tilt < self.max_rotation:
                self.tilt = self.max_rotation
        else:
            if self.tilt > -100:
                self.tilt -= self.rot_velocity

    def draw(self, win):

        self.img_count += 1

        if self.img_count < self.animation_time:
            self.img = self.images[0]
        elif self.img_count < self.animation_time * 2:
            self.img = self.images[1]
        elif self.img_count < self.animation_time * 3:
            self.img = self.images[2]
        elif self.img_count < self.animation_time * 4:
            self.img = self.images[1]
        elif self.img_count == self.animation_time * 4 + 1:
            self.img = self.images[0]
            self.img_count = 0

        if self.tilt <= -90:
            self.img = self.images[0]
            self.img_count = self.animation_time * 2

        rotate_image = pygame.transform.rotate(self.img, self.tilt)
        new_react = rotate_image.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)
        win.blit(rotate_image, new_react)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)
