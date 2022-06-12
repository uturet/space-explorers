import pygame
from abc import ABC, abstractmethod
from core.config import Config
from core import collision_handler as ch
from core.animation import Frame


class Building(pygame.sprite.Sprite):
    size = 0
    is_hover = False
    is_active = False
    building_con = {}

    def __init__(self,  building_con, pos):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.building_con = building_con
        for building, con in building_con.items():
            building.add_connection(self, con)
            con.connects.add(self)
        self._image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        self.rect = self._image.get_rect()
        self.rect.center = pos
        self.paint()
        self.mask = pygame.mask.from_surface(self._image)

    def draw(self, state):
        pass

    def activate(self):
        pass

    def deacticate(self):
        pass

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


class Preview(ABC):
    building = None
    valid = True

    height = 0
    width = 0
    cover_size = 200
    cover_radius = 100
    option_radius = 0
    small_option_radius = 0

    color = Config.black
    preview_color = Config.black
    invalid_preview_color = Config.pink_500

    connections = {}

    def __init__(self):
        self._image = pygame.Surface(
            (self.width, self.height), pygame.SRCALPHA)
        self.option_image = pygame.Surface(
            (Config.hotbarheight, Config.hotbarheight), pygame.SRCALPHA)
        self.cover_image = pygame.Surface(
            (self.cover_size, self.cover_size), pygame.SRCALPHA)

        self.option_rect = self.option_image.get_rect()
        self.cover_rect = self.cover_image.get_rect()
        self.rect = self._image.get_rect()

        self.frames = []
        self.create_preview_frames()

    def update_preview_image(self, state=None, image=None, valid=True):
        self.valid = valid
        if state and image and valid:
            for line in self.connections.values():
                line.calculate_abs_pos(image, state.mouse.bg_rect.center)
        if valid:
            self.image = self.frames[0].image
            self.mask = self.frames[0].mask
        else:
            self.image = self.frames[1].image
            self.mask = self.frames[1].mask

    @abstractmethod
    def create_preview_frames(self):
        pass

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


class Connectoin(pygame.sprite.Sprite):
    groups = ()
    connects = set()
    line_width = 4

    def __init__(self, start_pos, spr):
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.connects = {spr}
        end_pos = spr.rect.center

        rect = ch.rect_from_points(start_pos, end_pos)
        rect.h = max(self.line_width, rect.h)
        rect.w = max(self.line_width, rect.w)

        self.frames = []

        coords = self.calculate_bg_pos(rect, start_pos, end_pos)
        for i, color in enumerate((Config.indigo_300, Config.orange_400)):
            image = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
            self.rect = image.get_rect()
            self.rect.center = rect.center
            pygame.draw.line(image, color,
                             *coords, int(self.line_width))
            converted = image.convert_alpha()
            self.frames.append(
                Frame(converted, pygame.mask.from_surface(converted)))

        self.image = self.frames[0].image
        self.mask = self.frames[0].mask

    def activate(self):
        self.image = self.frames[1].image
        self.mask = self.frames[1].mask

    def deactivate(self):
        self.image = self.frames[0].image
        self.mask = self.frames[0].mask

    def draw(self, state):
        state.screen.blit(
            self.image, state.bg.bg_pos_to_abs(*self.rect.topleft))

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
