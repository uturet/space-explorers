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
    invalid_preview_color = Config.red_200

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

        image = pygame.Surface(
            (self.width, self.height), pygame.SRCALPHA)
        pygame.draw.circle(image, self.preview_color,
                           self.rect.center, self.radius)
        converted = image.convert_alpha()
        self.images.append((converted, pygame.mask.from_surface(converted)))

        image = pygame.Surface(
            (self.width, self.height), pygame.SRCALPHA)
        pygame.draw.circle(image, self.invalid_preview_color,
                           self.rect.center, self.radius)
        converted = image.convert_alpha()
        self.images.append((converted, pygame.mask.from_surface(converted)))

    def update_preview_image(self, valid=True):
        # self.image.set_alpha(100)
        self._image.fill((255, 255, 255, 100))
        for line in self.lines:
            self.cover_image.blit(line.image, line.rect)
        if valid:
            self.image = self.images[0][0]
            self.mask = self.images[0][1]
        else:
            self.image = self.images[1][0]
            self.mask = self.images[1][1]

    @ abstractmethod
    def draw_option_image(self, image, rect):
        pass

    @ abstractmethod
    def draw_small_option_image(self, image, rect):
        pass

    @ abstractmethod
    def draw_preview_image(self):
        pass

    @ abstractmethod
    def draw_invalid_preview_image(self):
        pass

    def handle_intersections(self, state, intersections):
        self.lines.clear()
        for sp in intersections:
            if isinstance(sp, Building) and \
                ch.circle_intersects_circle(
                    state.mouse.bg_rect.center, self.cover_radius,
                    sp.rect.center, sp.radius
            ):
                pos = state.bg.bg_pos_to_abs(sp.rect.centerx, sp.rect.centery)
                pos = (
                    pos[0]-state.mouse.rect.centerx+self.rect.centerx,
                    pos[1]-state.mouse.rect.centery+self.rect.centery
                )

                connection = Connectoin(self.rect.center, pos)
                col = pygame.sprite.collide_mask(sp, connection)
                if not col:
                    self.lines.add(connection)


class Connectoin(pygame.sprite.Sprite):
    groups = ()

    def __init__(self, start_pos, end_pos):
        rect = ch.rect_from_points(start_pos, end_pos)
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.center = rect.center
        pygame.draw.line(self.image, Config.pink_500, start_pos, end_pos)
        self.mask = pygame.mask.from_surface(self.image)


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
