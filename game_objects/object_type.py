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

    building_con = None
    hover_color = Config.blue_200
    active_color = Config.green_200

    def __init__(self,  building_con, pos):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.building_con = building_con
        for building, con in building_con.items():
            building.add_connection(self, con)
            con.connects.add(self)

        self.colors = (self.color, self.hover_color, self.active_color)
        self.create_frames(center=pos)
        self.select_frame(0)

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, i):
        if i in (self.INACTIVE, self.HOVERED, self.SELECTED):
            self._status = i
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

    cover_size = 200
    cover_radius = 100
    option_radius = 40
    small_option_radius = option_radius/2

    preview_color = Config.black
    invalid_preview_color = Config.pink_500

    connections = None

    def __init__(self):
        self.connections = {}
        self.width = self.building.width
        self.height = self.building.height
        self.radius = self.building.radius
        self.color = self.building.color
        self.colors = (self.preview_color, self.invalid_preview_color)

        self.option_image = pygame.Surface(
            (Config.hotbarheight, Config.hotbarheight), pygame.SRCALPHA)
        self.option_rect = self.option_image.get_rect()

        self.create_frames()
        self.select_frame(0)

    def update_preview_image(self, state=None, image=None, valid=True):
        if state and image and valid:
            for line in self.connections.values():
                line.calculate_abs_pos(image, state.mouse.bg_rect.center)
        if valid:
            self.select_frame(0)
        else:
            self.select_frame(1)

    @ abstractmethod
    def draw_option_image(self, rect, image=None):
        pass

    @ abstractmethod
    def draw_small_option_image(self, rect, image=None):
        pass

    def handle_intersections(self, state, intersections):
        self.connections.clear()
        for spr in intersections:
            if (isinstance(spr, Building) and
                ch.circle_intersects_circle(
                    state.mouse.bg_rect.center, self.cover_radius,
                    spr.rect.center, spr.radius
            )):
                connection = Connectoin(
                    state.mouse.bg_rect.center, spr)
                self.connections[spr] = connection
                for i in intersections:
                    if i != spr:
                        if (pygame.sprite.collide_mask(i, connection) and
                                i in self.connections):
                            del self.connections[i]


class Connectoin(pygame.sprite.Sprite, ColorFrameList):
    groups = ()
    connects = None
    line_width = 4

    def __init__(self, start_pos, spr):
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.connects = {spr}
        end_pos = spr.rect.center

        rect = ch.rect_from_points(start_pos, end_pos)
        rect.h = max(self.line_width, rect.h)
        rect.w = max(self.line_width, rect.w)

        self.width = rect.w
        self.height = rect.h
        self.colors = (Config.indigo_300, Config.orange_400)
        self.coords = self.calculate_bg_pos(rect, start_pos, end_pos)

        self.create_frames(center=rect.center)
        self.select_frame(0)

    def draw_frame(self, image, color):
        pygame.draw.line(image, color,
                         *self.coords, int(self.line_width))

    def activate(self):
        self.select_frame(1)

    def deactivate(self):
        self.select_frame(0)

    def calculate_abs_pos(self, image, pos):
        rect = self.rect.copy()
        center = (100, 100)
        if pos[0]-rect.left < self.rect.w/2:
            if pos[1]-rect.top < self.rect.h/2:
                rect.topleft = (100, 100)
            else:
                rect.bottomleft = center
        else:
            if pos[1]-rect.top < self.rect.h/2:
                rect.topright = center
            else:
                rect.bottomright = center

        image.blit(self.image, rect.topleft)

    def calculate_bg_pos(self, rect, start_pos, end_pos):
        coords = ((0, 0), (rect.w, rect.h))
        if start_pos[0] > end_pos[0]:
            if start_pos[1] < end_pos[1]:
                coords = ((rect.w, 0), (0, rect.h))
        if start_pos[0] < end_pos[0]:
            if start_pos[1] > end_pos[1]:
                coords = ((rect.w, 0), (0, rect.h))
        if rect.h == self.line_width:
            coords = ((0, rect.h/2), (rect.w, rect.h/2))
        if rect.w == self.line_width:
            coords = ((rect.w/2, 0), (rect.w/2, rect.h))
        return coords


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
