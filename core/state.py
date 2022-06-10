import pygame
from core.config import Config
import user_interface as ui
from game_objects import Transmitter
from core.event_manager import EventManager
from core import collision_handler as ch
from core.grid import Grid
from seeder import seed_buildings_rand
from core.event import HOTBARINFOMOD, HOTBARMULTIINFOMOD
from game_objects.buildings import building_previews, TransmitterPreview


class State:
    milliseconds = 0
    seconds = 0
    mouse_intersected = set()
    mouse_select = set()
    tmp_group = set()

    def __init__(self):
        self.screen = pygame.display.set_mode((Config.width, Config.height))
        self.set_group_attachmet()

        self.event_manager = EventManager(self)
        self.grid = Grid()

        self.bg = ui.Background()
        self.mouse = ui.Mouse()
        self.hotbar = ui.hotbar.Hotbar()
        self.minimap = ui.Minimap()

        seed_buildings_rand(200, self, (0, 0, Config.width, Config.height))
        # seed_buildings_rand(
        #     200, self, (2000, 2000, Config.width, Config.height))

        self.event_manager.add_group(
            self,
            *self.uigroup,
            self.bg,
            *self.interactable_group,
            self.mouse,
        )
        self.screen.blit(self.bg.image, self.bg.rect)

    def update(self):
        self.screen.fill(Config.bg)
        self.allgroup.update(self)

        self.screengroup.clear()
        self.grid.rect_intersects(self.bg.abs_rect, self.screengroup)
        # self.grid.draw_grid(self.screen)

        for spr in self.screengroup:
            spr.draw(self)
            self.screen.blit(
                spr.image, self.bg.bg_pos_to_abs(
                    spr.rect.left, spr.rect.top))
        self.uigroup.draw(self.screen)

    def handle_mousemotion(self, state, event):
        self.mouse_intersected.clear()
        self.tmp_group.clear()

        ch.get_rect_intersect_sprites_by_pos(
            event.pos,
            self.uigroup,
            self.mouse_intersected
        )
        ch.get_rect_intersect_sprites_by_pos(
            event.pos,
            self.interactable_group,
            self.mouse_intersected
        )

        if (self.minimap not in self.mouse_intersected and
            self.hotbar not in self.mouse_intersected and
                self.mouse.active_mod == self.mouse.INACTIVE):
            self.grid.pos_intersects(
                self.bg.abs_pos_to_bg(*event.pos), self.tmp_group)
            self.mouse_intersected.update(self.tmp_group)

    def handle_mousepreselect(self, state, event):
        self.mouse_select.clear()
        for spr in self.gamegroup:
            spr.is_hover = False
            spr.is_active = False

    def handle_mouseselect(self, state, event):
        prev_select = self.mouse_select.copy()
        self.mouse_select.clear()
        self.grid.rect_intersects(event.rect, self.mouse_select)

        for spr in (prev_select - self.mouse_select):
            spr.is_hover = False
        for spr in self.mouse_select:
            spr.is_hover = True

    def handle_mouseendselect(self, state, event):
        for spr in self.mouse_select:
            spr.is_hover = False
            spr.is_active = True
        if len(self.mouse_select) > 1:
            pygame.event.post(
                pygame.event.Event(
                    HOTBARMULTIINFOMOD,
                    {'sprites': self.mouse_select}
                ))
        elif len(self.mouse_select) == 1:
            pygame.event.post(
                pygame.event.Event(
                    HOTBARINFOMOD,
                    {'sprite': tuple(self.mouse_select)[0]}
                ))
        else:
            self.hotbar.set_active_mod(self.hotbar.DEFAULT_MOD)

    def set_group_attachmet(self):
        self.screengroup = set()
        self.allgroup = pygame.sprite.Group()
        self.uigroup = pygame.sprite.LayeredUpdates()
        self.interactable_group = pygame.sprite.Group()
        self.gamegroup = pygame.sprite.Group()

        Transmitter._layer = 3

        Transmitter.groups = (self.allgroup, self.gamegroup)

        ui.Background._layer = 1
        ui.Mouse._layer = 2
        ui.Minimap._layer = 9
        ui.hotbar.Hotbar._layer = 9

        ui.Node.groups = (self.interactable_group)

        ui.Mouse.groups = (self.allgroup, self.uigroup)
        ui.hotbar.Hotbar.groups = (self.allgroup, self.uigroup)
        ui.Background.groups = (self.allgroup)
        ui.Minimap.groups = (self.allgroup, self.uigroup)

        building_previews['Transmitter'] = TransmitterPreview()
