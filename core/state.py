import pygame
from core.config import Config
import user_interface as ui
from game_objects.buildings import Transmitter
from game_objects.object_type import Building
from core.event_manager import EventManager
from core import collision_handler as ch
from core.grid import Grid
from seeder import seed_buildings_rand
from core.event import HOTBARINFOMOD, HOTBARMULTIINFOMOD, HIGLIGHT
from game_objects.buildings import building_previews, TransmitterPreview, GeneratorPreview
from core.path_manager import PathManager
import random
from core.connection_manager import ConnectionManager


class State:
    milliseconds = 0
    seconds = 0
    secounds_past = 0

    def __init__(self):
        self.mouse_intersected = set()
        self.mouse_select = set()
        self.tmp_event_group = set()
        self.tmp_preview_group = {}
        self.buildgroup = set()
        self.congroup = set()
        self.partgroup = set()

        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen = pygame.display.set_mode((Config.width, Config.height))
        self.set_group_attachmet()

        self.event_manager = EventManager(self)
        self.grid = Grid()
        self.path_manager = PathManager()
        self.connection_manager = ConnectionManager()

        self.bg = ui.Background()
        self.mouse = ui.Mouse()
        self.hotbar = ui.hotbar.Hotbar()
        self.minimap = ui.Minimap()

        # pygame.time.set_timer(HIGLIGHT, 1000)

        seed_buildings_rand(1, self, self.screen.get_rect())

        self.event_manager.add_group(
            self,
            *self.uigroup,
            self.bg,
            *self.interactable_group,
            self.mouse,
        )
        self.screen.blit(self.bg.image, self.bg.rect)

    def handle_higlight(self, state, event):
        self.secounds_past += self.seconds

        for spr in self.gamegroup:
            spr.set_ui_type(Building.INACTIVE)

        for consumer, producers in self.path_manager.producers.items():
            if not len(producers):
                continue

            for paths in producers.values():
                path = paths[random.randint(0, len(paths)-1)]
                for i, v in enumerate(path):
                    if i == 0:
                        consumer.building_con[v].activate()
                    if i < (len(path)-1):
                        try:
                            v.building_con[path[i+1]].activate()
                        except Exception:
                            pass

    def draw_group(self, group):
        while group:
            spr = group.pop()
            self.screen.blit(
                spr.image, self.bg.bg_pos_to_abs(
                    spr.rect.left, spr.rect.top))

    def update(self):
        self.screen.fill(Config.bg)
        self.allgroup.update(self)

        self.grid.rect_intersects(
            self.bg.abs_rect,
            self.buildgroup,
            self.congroup,
            self.partgroup,
        )
        self.grid.draw_grid(self.screen)

        self.draw_group(self.congroup)

        for spr in self.tmp_preview_group.values():
            self.screen.blit(
                spr.image, self.bg.bg_pos_to_abs(
                    spr.rect.left, spr.rect.top))

        self.draw_group(self.buildgroup)
        self.draw_group(self.partgroup)

        self.uigroup.draw(self.screen)

    def handle_mousemotion(self, state, event):
        self.mouse_intersected.clear()
        self.tmp_event_group.clear()
        self.tmp_preview_group.clear()

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
                self.bg.abs_pos_to_bg(*event.pos), self.tmp_event_group)
            self.mouse_intersected.update(self.tmp_event_group)

    def handle_mousepreselect(self, state, event):
        while self.mouse_select:
            spr = self.mouse_select.pop()
            spr.set_ui_type(Building.INACTIVE)

    def handle_mouseselect(self, state, event):
        pass

    def handle_mouseendselect(self, state, event):

        self.grid.rect_intersects(event.rect, self.mouse_select)
        for spr in self.mouse_select:
            spr.set_ui_type(Building.SELECTED)
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
        self.allgroup = pygame.sprite.Group()
        self.uigroup = pygame.sprite.LayeredUpdates()
        self.interactable_group = pygame.sprite.Group()
        self.gamegroup = pygame.sprite.Group()

        Building._layer = 3

        Building.groups = (self.allgroup, self.gamegroup)

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
        building_previews['Generator'] = GeneratorPreview()

    def add_gameobj(self, obj):
        self.grid.add_item(obj)
        if isinstance(obj, Building):
            self.path_manager.add_building(obj)

    def create_selected_building(self, preview):
        new_building = preview.building(self.mouse.bg_rect.center)
        for building, con_prev in self.tmp_preview_group.items():
            con = con_prev.create_connection(self, new_building, building)
            new_building.add_connection(building, con)
            building.add_connection(new_building, con)
            if building.type == Building.ACTIVE:
                self.add_gameobj(con)
        self.add_gameobj(new_building)
        self.tmp_preview_group.clear()
