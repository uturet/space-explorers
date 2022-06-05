import pygame
import math
from config import Config
from user_interface import Minimap, Background, Mouse, Hotbar


class State():
    move_bg = set()
    mouse_int_sprites = set()

    def __init__(self):
        self.allgroup = pygame.sprite.LayeredUpdates()
        self.bggroup = pygame.sprite.Group()
        self.intgroup = pygame.sprite.Group()
        self.gamegroup = pygame.sprite.Group()

        Background._layer = 1
        Minimap._layer = 9
        Hotbar._layer = 9

        Hotbar.groups = (self.allgroup, self.gamegroup)
        Background.groups = (self.allgroup, self.gamegroup)
        Minimap.groups = (self.allgroup, self.intgroup)

        self.screen = pygame.display.set_mode((Config.width, Config.height))
        self.bg = Background()
        self.hotbar = Hotbar()
        self.mouse = Mouse(self.bg)
        self.minimap = Minimap()

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((Config.width, Config.height))

    def get_circular_intersect_sprites_by_pos(self, pos, sprites):
        for sp in sprites:
            if math.hypot(pos[0] - sp.pos[0], pos[1] - sp.pos[1]) < sp.radius:
                self.mouse_int_sprites.add(sp)

    def get_rect_intersect_sprites_by_pos(self, pos, sprites):
        for sp in sprites:
            if abs(sp.rect.left - pos[0]) < Config.minimapwidth and \
                    abs(sp.rect.bottom - pos[1]) < Config.minimapheight:
                self.mouse_int_sprites.add(sp)

    def update(self):
        self.mouse_int_sprites.clear()
        self.get_rect_intersect_sprites_by_pos(
            self.mouse.pos,
            self.intgroup
        )

        self.screen.fill(Config.dark)
        self.allgroup.update(self)
        self.allgroup.draw(self.screen)

        self.bggroup.update()

        for move in self.move_bg:
            move()
