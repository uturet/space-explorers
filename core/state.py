import pygame
from core.config import Config
from user_interface import Minimap, Background, Mouse, Hotbar
from game_objects import Transmitter
from core.event_manager import EventManager
from core import collision_handler as ch
from core.grid import Grid
from seeder import seed_buildings_rand


class State:
    mouse_intersected = set()
    tmp_group = set()

    def __init__(self):
        self.set_group_attachmet()

        self.event_manager = EventManager(self)
        self.grid = Grid()

        self.screen = pygame.display.set_mode((Config.width, Config.height))
        self.bg = Background()
        self.mouse = Mouse()
        self.hotbar = Hotbar(self.interactable_group)
        self.minimap = Minimap()

        # self.grid.draw_grid(self.bg.image)
        # seed_buildings_rand(100, self)

        self.clock = pygame.time.Clock()

        self.event_manager.add_group(
            self,
            *self.uigroup,
            *self.interactable_group,
            *self.gamegroup,
            self.mouse,
        )
        self.screen.blit(self.bg.image, self.bg.rect)

    def update(self):
        # self.screen.fill(Config.bg)
        self.allgroup.update(self)

        self.screengroup.clear()
        self.grid.rect_intersects(self.bg.abs_rect, self.screengroup)

        for spr in self.screengroup:
            self.bg.image.blit(spr.image, spr.rect)
        self.uigroup.draw(self.screen)

    def handle_mousemotion(self, state, event):
        self.mouse_intersected.clear()
        self.tmp_group.clear()
        self.mouse.rect.center = event.pos
        self.mouse.bg_rect.center = self.bg.abs_pos_to_bg(
            event.pos[0], event.pos[1])

        ch.get_rect_intersect_sprites_by_pos(
            self.mouse.rect.center,
            self.uigroup,
            self.mouse_intersected
        )
        ch.get_rect_intersect_sprites_by_pos(
            self.mouse.rect.center,
            self.interactable_group,
            self.mouse_intersected
        )

        if (self.minimap not in self.mouse_intersected and
            self.hotbar not in self.mouse_intersected and
                self.mouse.active_mod == self.mouse.INACTIVE):
            self.grid.pos_intersects(event.pos, self.tmp_group)
            self.mouse_intersected.update(self.tmp_group)

    def set_group_attachmet(self):
        self.screengroup = set()
        self.allgroup = pygame.sprite.Group()
        self.uigroup = pygame.sprite.LayeredUpdates()
        self.bggroup = pygame.sprite.LayeredUpdates()
        self.interactable_group = pygame.sprite.Group()
        self.gamegroup = pygame.sprite.Group()

        Transmitter._layer = 3

        Transmitter.groups = (self.allgroup, self.bggroup, self.gamegroup)

        Background._layer = 1
        Mouse._layer = 2
        Minimap._layer = 9
        Hotbar._layer = 9

        Mouse.groups = (self.allgroup, self.uigroup)
        Hotbar.groups = (self.allgroup, self.uigroup)
        Background.groups = (self.allgroup, self.uigroup)
        Minimap.groups = (self.allgroup, self.uigroup)
