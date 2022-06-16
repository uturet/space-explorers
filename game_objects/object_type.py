import pygame
from abc import ABC, abstractmethod
from core.config import Config
from core import collision_handler as ch
from core.property import EnergyInteraction
from core.event import HOTBARINFOMOD
from core.animation import ColorFrameList, Frame


class Building(pygame.sprite.Sprite, EnergyInteraction, ColorFrameList):

    health = 0
    health_point = 0

    INACTIVE = 0
    HOVERED = 1
    SELECTED = 2
    _ui_type = INACTIVE

    PLAN = 0
    ACTIVE = 1
    _type = PLAN

    _default_ei_type = EnergyInteraction.LATENT

    hover_color = Config.yellow_400
    active_color = Config.green_400

    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.building_con = {}
        self.frameset = []
        self.colors = (Config.bluegrey_400, self.color)
        self.create_frame_set(pos)
        self.select_frame()

    def receie_energy(self, state, charge):
        self.health_point += charge
        if self.health_point >= self.health:
            self.health_point = self.health
            if self._type == Building.PLAN:
                self.activate(state)

    def activate(self, state):
        self._type = Building.ACTIVE
        self._ei_type = self._default_ei_type
        state.path_manager.remove_consumer(self)
        state.path_manager.add_building(self)
        self.select_frame()

    def create_frame_set(self, pos):
        for color in self.colors:
            frames = []
            image = pygame.Surface(
                (self.width, self.height), pygame.SRCALPHA)
            self.draw_frame(image, color)
            self.add_frame(image, pos, frames)

            image = pygame.Surface(
                (self.width, self.height), pygame.SRCALPHA)
            self.draw_frame(image, color)
            pygame.draw.circle(image, self.hover_color,
                               (self.width/2, self.height/2), self.radius, 2)
            self.add_frame(image, pos, frames)

            image = pygame.Surface(
                (self.width, self.height), pygame.SRCALPHA)
            self.draw_frame(image, color)
            pygame.draw.circle(image, self.active_color,
                               (self.width/2, self.height/2), self.radius, 2)
            self.add_frame(image, pos, frames)

            self.frameset.append(frames)

    def add_frame(self, image, pos, frames):
        rect = image.get_rect()
        rect.center = pos
        converted = image.convert_alpha()
        frames.append(
            Frame(converted, rect, pygame.mask.from_surface(converted)))

    def select_frame(self):
        self.image = self.frameset[self.type][self.ui_type].image
        self.rect = self.frameset[self.type][self.ui_type].rect
        self.mask = self.frameset[self.type][self.ui_type].mask

    @property
    def ui_type(self):
        return self._ui_type

    def set_ui_type(self, index):
        self._ui_type = index
        self.select_frame()

    @property
    def type(self):
        return self._type

    def set_type(self, index):
        self._type = index
        self.select_frame()

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
        self.con_intersections = set()
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
        self.con_intersections.clear()
        state.grid.rect_intersects(
            state.mouse.bg_rect, self.intersections, self.con_intersections)

        self.valid = True
        for spr in self.intersections:
            if pygame.sprite.collide_mask(spr, self):
                self.valid = False
                break
        for spr in self.con_intersections:
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
