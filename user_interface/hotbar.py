import pygame
from config import Config
from seeder import seed_players_rand_static


class BuildingSelector(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(
            (Config.hotbarwidth * 2, Config.hotbarheight - 20))
        self.paintbar()
        self.rect = self.image.get_rect()
        self.rect.center = (10, 10)

        seed_players_rand_static(50, self)
        self.image = self.image.convert()

    def paintbar(self):
        self.image.fill(Config.bluegrey_500)

    def update(self, state):
        pass
        # self.paintbar()
        # seed_players_rand_static(50, self)

    def handle_mousewheel(self, state, event):
        self.rect.center = (
            self.rect.center[0] + ((event.x+event.y) * Config.scroll_speed),
            self.rect.center[1]
        )


class InfoBar(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

    def paintbar(self):
        self.image.fill(Config.bluegrey_500)

    def update(self, state):
        self.paintbar()

    def handle_mousewheel(self, state, event):
        pass


class MultiInfoBar(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

    def paintbar(self):
        self.image.fill(Config.bluegrey_500)

    def update(self, state):
        self.paintbar()

    def handle_mousewheel(self, state, event):
        pass


class Hotbar(pygame.sprite.Sprite):

    BUILDING_SELECTOR = 0
    INFOBAR = 1
    MULTI_INFOBAR = 2

    DEFAULT_MOD = 0

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface(
            (Config.hotbarwidth, Config.hotbarheight))
        self.paintbar()
        self.rect = self.image.get_rect()
        self.rect.midbottom = (round(Config.width / 2), Config.height)

        self.building_selector = BuildingSelector()
        self.infobar = InfoBar()
        self.multi_infobar = MultiInfoBar()

        self.mods = (self.building_selector, self.infobar, self.multi_infobar)

        self._active_mod = self.DEFAULT_MOD

    def get_mod(self):
        return self.mods[self._active_mod]

    def paintbar(self):
        self.image.fill(Config.dark)

    def update(self, state):
        self.paintbar()
        self.image.blit(self.get_mod().image, self.get_mod().rect.center)
        self.get_mod().update(state)

    def handle_mousewheel(self, state, event):
        if self in state.mouse_int_sprites:
            self.get_mod().handle_mousewheel(state, event)
