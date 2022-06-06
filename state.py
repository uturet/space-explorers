import pygame
import math
from config import Config
from user_interface import Minimap, Background, Mouse, MouseTracker, Hotbar
from user_interface import Node


class State():
    move_bg = set()
    mouse_int_sprites = set()

    def __init__(self):
        self.allgroup = pygame.sprite.LayeredUpdates()
        self.uigroup = pygame.sprite.Group()
        self.bggroup = pygame.sprite.Group()
        self.interactable_group = pygame.sprite.Group()
        self.gamegroup = pygame.sprite.Group()

        Background._layer = 1
        MouseTracker._layer = 8
        Minimap._layer = 9
        Hotbar._layer = 9

        MouseTracker.groups = (self.allgroup, self.uigroup)
        Hotbar.groups = (self.allgroup, self.uigroup)
        Background.groups = (self.allgroup, self.uigroup)
        Minimap.groups = (self.allgroup, self.uigroup)

        self.screen = pygame.display.set_mode((Config.width, Config.height))
        self.bg = Background()
        self.mouse = Mouse(self.bg)
        self.mouse_tracker = MouseTracker(self.screen)
        self.hotbar = Hotbar(self.interactable_group)
        self.minimap = Minimap()

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((Config.width, Config.height))

    def get_circular_intersect_sprites_by_pos(self, pos, sprites):
        for sp in sprites:
            if math.hypot(pos[0] - sp.pos[0], pos[1] - sp.pos[1]) < sp.radius:
                self.mouse_int_sprites.add(sp)

    def get_rect_intersect_sprites_by_pos(self, pos, sprites):
        for sp in sprites:
            if isinstance(sp, Node):
                coords = sp.calculate_abs_coords()
            else:
                coords = sp.rect
            if coords.left < pos[0] < coords.right and \
                    coords.top < pos[1] < coords.bottom:
                self.mouse_int_sprites.add(sp)

    def calculate_mouse_int_sprites(self):
        self.mouse_int_sprites.clear()
        self.get_rect_intersect_sprites_by_pos(
            self.mouse.pos,
            self.uigroup
        )
        self.get_rect_intersect_sprites_by_pos(
            self.mouse.pos,
            self.interactable_group
        )

    def update(self):
        self.calculate_mouse_int_sprites()

        self.screen.fill(Config.dark)
        self.allgroup.update(self)
        self.uigroup.draw(self.screen)

        for move in self.move_bg:
            move()
