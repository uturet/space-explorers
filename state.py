import pygame
import math
from config import Config
from radarmap import Radarmap


class Mouse:
    pos = (Config.width/2, Config.height/2)

    def __init__(self, bg):
        self._bg = bg

    @property
    def pos_x(self):
        x = round(
            self.pos[0] - (self._bg.pos[0] - (self._bg.dimens[0]/2)))
        return max(0, min(x, self._bg.dimens[0]))

    @property
    def pos_y(self):
        y = round(
            self.pos[1] - (self._bg.pos[1] - (self._bg.dimens[1]/2)))
        return max(0, min(y, self._bg.dimens[1]))

    @property
    def bg_bos(self):
        return (self.pos_x, self.pos_y)


class Background(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.dimens = (Config.bigmapwidth, Config.bigmapheight)
        self.image = pygame.Surface(self.dimens)
        self.image.fill(Config.bg)
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)

    @property
    def pos(self):
        return self.rect.center

    def hanlde_mausemotion(self, state, event):
        state.move_bg = set()
        if Config.width*Config.move_area > event.pos[0]:
            state.move_bg.add(self.move_left)
        if (Config.width - Config.width*Config.move_area) < event.pos[0]:
            state.move_bg.add(self.move_right)
        if Config.height*Config.move_area > event.pos[1]:
            state.move_bg.add(self.move_top)
        if (Config.height - Config.height*Config.move_area) < event.pos[1]:
            state.move_bg.add(self.move_bot)

    def move_left(self):
        self.rect.center = (
            min(round(self.dimens[0]/2), self.rect.center[0] + Config.speed),
            self.rect.center[1]
        )

    def move_right(self):
        self.rect.center = (
            max(Config.width - round(self.dimens[0]/2),
                self.rect.center[0] - Config.speed),
            self.rect.center[1]
        )

    def move_top(self):
        self.rect.center = (
            self.rect.center[0],
            min(round(self.dimens[1]/2), self.rect.center[1] + Config.speed)
        )

    def move_bot(self):
        self.rect.center = (
            self.rect.center[0],
            max(Config.height - round(self.dimens[1]/2),
                self.rect.center[1] - Config.speed)
        )


class State:
    move_bg = set()
    mouse_int_sprites = set()

    def __init__(self):
        self.allgroup = pygame.sprite.LayeredUpdates()
        self.bggroup = pygame.sprite.Group()

        Background._layer = 1
        Radarmap._layer = 9

        Background.groups = self.allgroup
        Radarmap.groups = self.allgroup

        self.screen = pygame.display.set_mode((Config.width, Config.height))
        self.bg = Background()
        self.mouse = Mouse(self.bg)
        self.radarmap = Radarmap()

        self.clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode((Config.width, Config.height))

    def get_intersect_sprites_by_pos(self, pos, sprites):
        int_sprites = set()
        for sp in sprites:
            if math.hypot(pos[0] - sp.pos[0], pos[1] - sp.pos[1]) < sp.radius:
                int_sprites.add(sp)
        return int_sprites

    def update(self):
        # self.mouse_int_sprites = self.get_intersect_sprites_by_pos(
        #     self.mouse.bg_bos,
        #     self.allgroup
        # )

        self.screen.fill(Config.dark)
        self.allgroup.update(self)
        self.allgroup.draw(self.screen)

        self.bggroup.update()

        for move in self.move_bg:
            move()
