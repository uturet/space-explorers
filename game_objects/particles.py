

from game_objects.object_type import Particle
import pygame
from core.config import Config
import math


class LightBeem(Particle):
    light_density = 2
    damage = 50
    distance = light_density * damage * 10
    fire = False

    def __init__(self, pos):
        super().__init__()
        self._image = pygame.Surface(
            (self.distance, self.light_density), pygame.SRCALPHA)
        self._image.fill((*Config.yellow_500, 255))

        self.image = self._image.convert_alpha()
        self.rect = self._image.get_rect()
        self.rect.midleft = pos
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, state):
        if not self.fire:
            return
        collision = None
        collided_spr = None
        for spr in state.gamegroup:
            col = pygame.sprite.collide_mask(self, spr)
            if col:
                if collision is None:
                    collision = col
                    collided_spr = spr
                elif (math.hypot(*collision) > math.hypot(*col)):
                    collision = col
                    collided_spr = spr

        if collision:
            collided_spr.receive_damage(
                state, round(state.seconds * self.damage))
            state.screen.blit(
                self.image, state.bg.bg_pos_to_abs(
                    *self.rect.topleft),
                (0, 0, math.hypot(*collision), 10))

        else:
            state.screen.blit(
                self.image, state.bg.bg_pos_to_abs(
                    *self.rect.topleft),
                (0, 0, self.distance, 10))
