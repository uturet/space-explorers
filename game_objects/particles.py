

from game_objects.object_type import Particle
import pygame
from core.config import Config
import math
from core import helpers as ch


class LightBeem(Particle):
    light_density = 2
    damage = 50
    distance = light_density * damage * 10
    fire = False

    def __init__(self, pos, angle):
        super().__init__()
        self.image = pygame.Surface(
            (self.distance, self.distance), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        start_pos = ch.get_line(
            self.rect.center,
            self.rect.midright,
            angle, 22)
        end_pos = ch.get_line(
            self.rect.center,
            self.rect.midright,
            angle, self.distance//2)
        pygame.draw.line(self.image, Config.yellow_500,
                         start_pos, end_pos, self.light_density)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = pos
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
                    *self.rect.topleft))

        else:
            state.screen.blit(
                self.image, state.bg.bg_pos_to_abs(
                    *self.rect.topleft))
