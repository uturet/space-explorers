import pygame
from abc import ABC, abstractclassmethod
from core.config import Config


class Building(pygame.sprite.Sprite):
    size = 0
    is_hover = False
    is_active = False

    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self._image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        self.rect = self._image.get_rect()
        self.rect.center = pos

    @classmethod
    def get_option_image(cls):
        pass

    @classmethod
    def get_preview_image(cls):
        pass


class Preview(ABC):
    building = None

    cover_size = 0
    cover_radius = 0
    option_radius = 0

    color = Config.black
    preview_color = Config.black

    def __init__(self):
        self.option_image = self.get_option_image()
        self.preview_image = self.get_preview_image()

        self.option_rect = self.option_image.get_rect()
        self.preview_rect = self.preview_image.get_rect()

    @abstractclassmethod
    def get_option_image(self):
        pass

    @abstractclassmethod
    def get_preview_image(self):
        pass

    @abstractclassmethod
    def handle_collisions(self, state, collisions):
        pass


class Particle(pygame.sprite.Sprite):
    pos = [0, 0]
    vel = [0, 0]
    accel = [0, 0]
    dt = 1.0/Config.fps

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.groups)

    def update(self):
        """Collision Detection"""
        self.vel[0] += self.accel[0] * self.dt
        self.pos[0] += self.vel[0] * self.dt

        self.vel[1] += self.accel[1] * self.dt
        self.pos[1] += self.vel[1] * self.dt

    def handle_box_collision(self, box):
        """Discrete collision detection
            Sweep and Prune
            Space Partitions
                Uniform grid partition
                Smarter Space Partitioning 
                    K-D Trees
            Object Partitions
                Bounding Volume Hierarchies
        """
        """Continuous collision detection"""
        if self.left[0] <= box.left[0] or \
                self.right[0] >= box.right[0]:
            self.vel[0] = -self.vel[0]
        if self.bottom[1] <= box.bottom[1] or \
                self.top[1] >= box.top[1]:
            self.vel[1] = -self.vel[1]
