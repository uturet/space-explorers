import user_interface as ui
from game_objects.buildings import Building
from core.config import Config
from abc import ABC
import pygame


class Hotbar(pygame.sprite.Sprite, ui.Node):

    BUILDING_SELECTOR = 0
    INFOBAR = 1
    MULTI_INFOBAR = 2

    DEFAULT_MOD = 0
    active_mod_index = 0

    def __init__(self, parent=None):
        pygame.sprite.Sprite.__init__(self, self.groups)
        ui.Node.__init__(self, parent)
        self.image = pygame.Surface(
            (Config.hotbarwidth, Config.hotbarheight))
        self.paintbar()
        self.rect = self.image.get_rect()
        self.rect.topleft = (
            round(Config.width / 2) - round(Config.hotbarwidth/2),
            Config.height - Config.hotbarheight
        )

        self.building_selector = ui.BuildingSelector(parent=self)
        self.infobar = ui.InfoBar(parent=self)
        self.multi_infobar = ui.MultiInfoBar(parent=self)
        self.mods = (self.building_selector, self.infobar, self.multi_infobar)

    def handle_selected(self, selected=None):
        if selected is None:
            self.active_mod_index = self.DEFAULT_MOD
        elif isinstance(selected, Building):
            self.active_mod_index = self.INFOBAR
        elif type(selected) is list:
            self.active_mod_index = self.MULTI_INFOBAR

    def handle_hotbarinfomod(self, state, event):
        self.active_mod_index = self.INFOBAR
        self.active_mod.set_info_provider(event.sprite)

    def handle_hotbarmultiinfomod(self, state, event):
        self.active_mod_index = self.MULTI_INFOBAR
        self.active_mod.set_info_providers(event.sprites)

    @property
    def active_mod(self):
        return self.mods[self.active_mod_index]

    def paintbar(self):
        self.image.fill(Config.dark)

    def update(self, state):
        self.paintbar()
        self.image.blit(self.active_mod.image, self.active_mod.rect.topleft)
        self.active_mod.update(state)


class HotbarMod(pygame.sprite.Sprite, ui.Node, ABC):
    hotbar_mod = None
    width = Config.hotbarwidth
    height = Config.hotbarheight - 20

    def __init__(self, parent=None):
        pygame.sprite.Sprite.__init__(self, self.groups)
        ui.Node.__init__(self, parent)

        self.image = pygame.Surface((self.width, self.height))
        self.paintbar()
        self.rect = self.image.get_rect()
        self.rect.topleft = (10, 10)

    def paintbar(self):
        self.image.fill(Config.bluegrey_500)

    def update(self, state):
        pass

    def is_hovered(self, state):
        return (state.hotbar in state.mouse_intersected and
                state.hotbar.active_mod_index == self.hotbar_mod and
                self in state.mouse_intersected)

    def handle_mousewheel(self, state, event):
        if self.is_hovered(state):
            pass
