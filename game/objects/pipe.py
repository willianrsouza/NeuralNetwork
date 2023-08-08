import random
import pygame
from game.env import pipe_image


class Pipe:
    gap = 200
    velocity = 5

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.gap = 200

        self.top = 0
        self.bottom = 0
        self.pipe_top = pygame.transform.flip(pipe_image(), False, True)
        self.pipe_bottom = pipe_image()

        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)

        self.top = self.height - self.pipe_top.get_height()
        self.bottom = self.height + self.gap

    def move(self):
        self.x -= self.velocity

    def draw(self, win):
        win.blit(self.pipe_top, (self.x, self.top))
        win.blit(self.pipe_bottom, (self.x, self.bottom))

    def get_top_mask(self):
        return pygame.mask.from_surface(self.pipe_top)

    def get_bottom_mask(self):
        return pygame.mask.from_surface(self.pipe_bottom)

    def collide(self, bird):
        bird_mask = bird.get_mask()
        pipe_bottom_mask = self.get_bottom_mask()
        pipe_top_mask = self.get_top_mask()

        # Verify overlap

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(pipe_bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(pipe_top_mask, top_offset)

        if t_point or b_point:
            return True

        return False
