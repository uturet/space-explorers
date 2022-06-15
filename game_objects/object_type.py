import pygame
from abc import ABC, abstractmethod
from core.config import Config
from core import collision_handler as ch
from core.property import EnergyInteraction
from core.event import HOTBARINFOMOD
from core.animation import ColorFrameList


class Building(pygame.sprite.Sprite, EnergyInteraction, ColorFrameList):

    INACTIVE = 0
    HOVERED = 1
    SELECTED = 2

    _status = INACTIVE

    hover_color = Config.blue_200
    active_color = Config.green_200

    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.building_con = {}

        self.colors = (self.color, self.hover_color, self.active_color)
        self.create_frames(center=pos)
        self.select_frame(0)

    @property
    def status(self):
        return self._status

    def set_status(self, index):
        if index in (self.INACTIVE, self.HOVERED, self.SELECTED):
            self._status = index
            self.select_frame(index)
        else:
            raise Exception(
                f'Invalid {self.__class__.__name___}.status. Should be one of {(self.INACTIVE, self.HOVERED, self.SELECTED)}, given {i}')

    def handle_mousebuttonup(self, state, event):
        if (self in state.mouse_intersected
                and self._status != self.SELECTED):
            self._status = self.SELECTED
            pygame.event.post(pygame.event.Event(
                HOTBARINFOMOD, {'sprite': self}))

    def add_connection(self, building, con):
        self.building_con[building] = con

    def remove_connection(self, building):
        del self.building_con[building]

    @classmethod
    def get_option_image(cls):
        pass

    @classmethod
    def get_preview_image(cls):
        pass


class Preview(ABC, ColorFrameList):
    building = None
    valid = True
    option_radius = 40
    small_option_radius = option_radius/2

    preview_color = Config.black
    invalid_preview_color = Config.pink_500

    def __init__(self):
        self.intersections = set()
        self.width = self.building.width
        self.height = self.building.height
        self.radius = self.building.radius
        self.color = self.building.color
        self.colors = (self.preview_color, self.invalid_preview_color)

        self.option_image = pygame.Surface(
            (Config.hotbarheight, Config.hotbarheight), pygame.SRCALPHA)
        self.option_rect = self.option_image.get_rect()
        self.center_point = (
            Config.preview_cover_radius - self.width/2,
            Config.preview_cover_radius - self.height/2)
        self.create_frames()
        self.select_frame(0)

    @ abstractmethod
    def draw_option_image(self, rect, image=None):
        pass

    @ abstractmethod
    def draw_small_option_image(self, rect, image=None):
        pass

    def handle_mousemotion(self, state, event):
        self.rect.center = state.mouse.bg_rect.center
        self.intersections.clear()
        state.grid.rect_intersects(state.mouse.bg_rect, self.intersections)

        self.valid = True
        for spr in self.intersections:
            if pygame.sprite.collide_mask(spr, self):
                self.valid = False
                break
        if self.valid:
            state.connection_manager.set_connections(
                state, self.intersections)
            self.select_frame(0)
        else:
            self.select_frame(1)
        state.mouse.image.blit(self.image, self.center_point)


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
        if (self.left[0] <= box.left[0] or
                self.right[0] >= box.right[0]):
            self.vel[0] = -self.vel[0]
        if (self.bottom[1] <= box.bottom[1] or
                self.top[1] >= box.top[1]):
            self.vel[1] = -self.vel[1]
