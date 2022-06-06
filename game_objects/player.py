import pygame
from core.config import Config
import itertools
import random


class Player(pygame.sprite.Sprite):
    radius = 100

    def __init__(self, pos, background):
        pygame.sprite.Sprite.__init__(self)

        self.background = background
        self.color = Config.blue
        self.colors = itertools.cycle(
            (Config.blue_light, Config.blue, Config.blue_dark, Config.blue))
        self.last_update = pygame.time.get_ticks()
        self.animation_cooldown = random.randint(500, 2000)
        size = 30
        self.rad = size/2
        self.pos = pos

        pygame.draw.circle(self.background, next(
            self.colors), pos, self.rad)

    def update(self):
        cur_time = pygame.time.get_ticks()
        if cur_time - self.last_update >= self.animation_cooldown:
            pygame.draw.circle(self.background, next(
                self.colors), self.pos, self.rad)
            self.last_update = cur_time

    def show_area(self, field):
        pygame.draw.circle(field.image, self.color, self.pos, self.radius, 1)
