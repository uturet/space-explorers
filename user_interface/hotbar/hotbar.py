from core.config import Config
import user_interface as ui
import pygame


class Hotbar(pygame.sprite.Sprite):

    SELECTMOD = 0
    INFOMOD = 1
    MULTI_INFOMOD = 2

    active_mod_index = SELECTMOD

    width = Config.hotbarwidth
    height = Config.hotbarheight

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface(
            (Config.hotbarwidth, Config.hotbarheight))

        self.rect = self.image.get_rect()
        self.rect.bottomleft = (
            round(Config.width / 2) - round(Config.hotbarwidth/2),
            Config.height - (Config.height * Config.move_area)
        )
        self.selectbar = ui.hotbar.Selectbar()
        self.infobar = ui.hotbar.InfoBar()
        self.multi_infobar = ui.hotbar.MultiInfoBar()
        self.mods = (self.selectbar, self.infobar, self.multi_infobar)
        self.draw()

    def handle_hotbarselectmod(self, state, event):
        self.set_active_mod(self.SELECTMOD)
        self.draw()

    def handle_hotbarinfomod(self, state, event):
        self.set_active_mod(self.INFOMOD)
        self.active_mod.set_info_provider(event.sprite)
        self.draw()

    def handle_hotbarmultiinfomod(self, state, event):
        self.set_active_mod(self.MULTI_INFOMOD)
        self.active_mod.set_info_providers(event.sprites)
        self.draw()

    def set_active_mod(self, mod_index):
        if mod_index in (
                self.SELECTMOD, self.INFOMOD, self.MULTI_INFOMOD):
            self.active_mod_index = mod_index
            self.draw()

    def handle_mousebuttondown(self, state, event):
        if hasattr(self.active_mod, 'handle_mousebuttondown'):
            event.pos = (event.pos[0] - self.rect.left,
                         event.pos[1] - self.rect.top)
            self.active_mod.handle_mousebuttondown(state, event)
            self.draw()

    def handle_mousebuttonup(self, state, event):
        if (hasattr(self.active_mod, 'handle_mousebuttonup')):
            event.pos = (event.pos[0] - self.rect.left,
                         event.pos[1] - self.rect.top)
            self.active_mod.handle_mousebuttonup(state, event)
            self.draw()

    def handle_mousewheel(self, state, event):
        if (hasattr(self.active_mod, 'handle_mousewheel')):
            self.active_mod.handle_mousewheel(state, event)
            self.draw()

    def handle_mousemotion(self, state, event):
        if (hasattr(self.active_mod, 'handle_mousemotion')):
            self.active_mod.handle_mousemotion(state, event)

    @property
    def active_mod(self):
        return self.mods[self.active_mod_index]

    def update(self, state):
        self.active_mod.update(state)

    def draw(self):
        self.image.fill(Config.grey_700)
        self.active_mod.draw()
        self.image.blit(self.active_mod.image, self.active_mod.rect.topleft)
