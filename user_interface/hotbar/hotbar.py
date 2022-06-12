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

        self.selectbar = ui.hotbar.Selectbar(parent=self)
        self.infobar = ui.hotbar.InfoBar(parent=self)
        self.multi_infobar = ui.hotbar.MultiInfoBar(parent=self)
        self.mods = (self.selectbar, self.infobar, self.multi_infobar)

    def handle_hotbarselectmod(self, state, event):
        self.set_active_mod(self.SELECTMOD)

    def handle_hotbarinfomod(self, state, event):
        self.set_active_mod(self.INFOMOD)
        self.active_mod.set_info_provider(event.sprite)

    def handle_hotbarmultiinfomod(self, state, event):
        self.set_active_mod(self.MULTI_INFOMOD)
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
