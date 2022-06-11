import pygame
from abc import ABC, abstractmethod
from core.config import Config
from core import collision_handler as ch


class Building(pygame.sprite.Sprite):
    size = 0
    is_hover = False
    is_active = False

    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self._image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        self.rect = self._image.get_rect()
        self.rect.center = pos
        self.paint()
        self.mask = pygame.mask.from_surface(self._image)

    def draw(self, state):
        pass

    @classmethod
    def get_option_image(cls):
        pass

    @classmethod
    def get_preview_image(cls):
        pass


class Preview(ABC):
    building = None

    height = 0
    width = 0
    cover_size = 0
    cover_radius = 0
    option_radius = 0
    small_option_radius = 0

    color = Config.black
    preview_color = Config.black
    invalid_preview_color = Config.pink_500

    lines = set()

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

        self.images = []

        for color in (self.preview_color, self.invalid_preview_color):
            image = pygame.Surface(
                (self.width, self.height), pygame.SRCALPHA)
            pygame.draw.circle(image, color,
                               self.rect.center, self.radius)
            converted = image.convert_alpha()
            self.images.append(
                (converted, pygame.mask.from_surface(converted)))

    def update_preview_image(self, state=None, image=None, valid=True):
        if state and image and valid:
            for line in self.lines:
                line.calculate_abs_pos(image, state.mouse.bg_rect.center)
        if valid:
            self.image = self.images[0][0]
            self.mask = self.images[0][1]
        else:
            self.image = self.images[1][0]
            self.mask = self.images[1][1]

    @ abstractmethod
    def draw_option_image(self, rect, image=None):
        pass

    @ abstractmethod
    def draw_small_option_image(self, rect, image=None):
        pass

    @ abstractmethod
    def draw_preview_image(self):
        pass

    @ abstractmethod
    def draw_invalid_preview_image(self):
        pass

    def handle_intersections(self, state, intersections):
        self.lines.clear()
        exclude_lines = set()
        for spr in intersections:
            if (isinstance(spr, Building) and
                ch.circle_intersects_circle(
                    state.mouse.bg_rect.center, self.cover_radius,
                    spr.rect.center, spr.radius
            )):
                connection = Connectoin(
                    state.mouse.bg_rect.center, spr.rect.center)
                self.lines.add(connection)
                for i in intersections:
                    if i != spr:
                        if pygame.sprite.collide_mask(i, connection):
                            exclude_lines.add(connection)
            self.lines -= exclude_lines


class Connectoin(pygame.sprite.Sprite):
    groups = ()

    line_width = 4

    def __init__(self, start_pos, end_pos):
        rect = ch.rect_from_points(start_pos, end_pos)
        rect.h = max(self.line_width, rect.h)
        rect.w = max(self.line_width, rect.w)
        pygame.sprite.Sprite.__init__(self, self.groups)
        self._image = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
        # self._image.fill((255, 255, 255, 100))
        self.rect = self._image.get_rect()
        self.rect.center = rect.center

        coords = ((0, 0), (self.rect.w, self.rect.h))
        if start_pos[0] > end_pos[0]:
            if start_pos[1] < end_pos[1]:
                coords = ((self.rect.w, 0), (0, self.rect.h))
        if start_pos[0] < end_pos[0]:
            if start_pos[1] > end_pos[1]:
                coords = ((self.rect.w, 0), (0, self.rect.h))

        if rect.h == self.line_width:
            coords = ((0, rect.h/2), (rect.w, rect.h/2))
        if rect.w == self.line_width:
            coords = ((rect.w/2, 0), (rect.w/2, rect.h))

        pygame.draw.line(self._image, Config.pink_500,
                         *coords, self.line_width)
        self.image = self._image.convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)

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
