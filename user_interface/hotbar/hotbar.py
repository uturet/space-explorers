import user_interface as ui
from game_objects.buildings import Building
from core.config import Config
from abc import ABC
import pygame


class Hotbar(pygame.sprite.Sprite):

    SELECTMOD = 0
    INFOMOD = 1
    MULTI_INFOMOD = 2

    DEFAULT_MOD = SELECTMOD
    active_mod_index = DEFAULT_MOD

    width = Config.hotbarwidth
    height = Config.hotbarheight

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface(
            (Config.hotbarwidth, Config.hotbarheight))
        self.paintbar()
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (
            round(Config.width / 2) - round(Config.hotbarwidth/2),
            Config.height
        )

        self.selectbar = ui.Selectbar(parent=self)
        self.infobar = ui.InfoBar(parent=self)
        self.multi_infobar = ui.MultiInfoBar(parent=self)
        self.mods = (self.selectbar, self.infobar, self.multi_infobar)

    def handle_selected(self, selected=None):
        if selected is None:
            self.active_mod_index = self.DEFAULT_MOD
        elif isinstance(selected, Building):
            self.active_mod_index = self.INFOMOD
        elif type(selected) is list:
            self.active_mod_index = self.MULTI_INFOMOD

    def handle_hotbarselectmod(self, state, event):
        self.active_mod_index = self.SELECTMOD

    def handle_hotbarinfomod(self, state, event):
        self.active_mod_index = self.INFOMOD
        self.active_mod.set_info_provider(event.sprite)

    def handle_hotbarmultiinfomod(self, state, event):
        self.active_mod_index = self.MULTI_INFOMOD
        self.active_mod.set_info_providers(event.sprites)

    def set_active_mod(self, mod_index):
        if mod_index in (
                self.SELECTMOD, self.INFOMOD, self.MULTI_INFOMOD):
            self.active_mod_index = mod_index

    @property
    def active_mod(self):
        return self.mods[self.active_mod_index]

    def paintbar(self):
        self.image.fill(Config.dark)

    def update(self, state):
        self.paintbar()
        self.image.blit(self.active_mod.image, self.active_mod.rect.topleft)
        self.active_mod.update(state)


class HotbarMod(ui.Node, ABC):
    hotbar_mod = None
    width = Config.hotbarwidth
    height = Config.hotbarheight

    def __init__(self, parent):
        ui.Node.__init__(self, parent)
        self.paintbar()
        self.rect.topleft = (0, 0)

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
