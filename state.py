import pygame
import math
from options import Options


class Mouse:
    pos = (Options.width/2, Options.height/2)

    def __init__(self, field):
        self._field = field

    @property
    def pos_x(self):
        x = round(
            self.pos[0] - (self._field.pos[0] - (self._field.dimens[0]/2)))
        return max(0, min(x, self._field.dimens[0]))

    @property
    def pos_y(self):
        y = round(
            self.pos[1] - (self._field.pos[1] - (self._field.dimens[1]/2)))
        return max(0, min(y, self._field.dimens[1]))

    @property
    def field_pos(self):
        return (self.pos_x, self.pos_y)


class Field(pygame.sprite.Sprite):

    def __init__(self):
        self.dimens = (4000, 4000)
        self.pos = [0, 0]
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(self.dimens)
        self.image.fill(Options.dark)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def move_left(self):
        self.pos[0] = min(self.dimens[0]/2, self.pos[0] + Options.speed)
        self.rect.center = self.pos

    def move_right(self):
        self.pos[0] = max(Options.width-self.dimens[0] /
                          2, self.pos[0] - Options.speed)
        self.rect.center = self.pos

    def move_top(self):
        self.pos[1] = min(self.dimens[1]/2, self.pos[1] + Options.speed)
        self.rect.center = self.pos

    def move_bot(self):
        self.pos[1] = max(Options.height-self.dimens[1] /
                          2, self.pos[1] - Options.speed)
        self.rect.center = self.pos


class State:
    move_field = set()
    new_items = set()

    def __init__(self):
        self.field = Field()
        self.mouse = Mouse(self.field)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((Options.width, Options.height))
        self.mouse_int_sprites = set()
        self.players_sprites = pygame.sprite.Group()
        self.interface_sprites = pygame.sprite.Group()
        self.interface_sprites.add(self.field)

    def get_intersect_sprites_by_pos(self, pos, sprites):
        int_sprites = set()
        for sp in sprites:
            if math.hypot(pos[0] - sp.pos[0], pos[1] - sp.pos[1]) < sp.radius:
                int_sprites.add(sp)
        return int_sprites

    def update(self):
        self.mouse_int_sprites = self.get_intersect_sprites_by_pos(
            self.mouse.field_pos,
            self.players_sprites
        )
