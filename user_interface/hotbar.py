import pygame
from config import Config
import itertools
from user_interface.node import Node


class SelectorOption(pygame.sprite.Sprite, Node):

    def __init__(self, size, shift, color, parent=None):
        pygame.sprite.Sprite.__init__(self, self.groups)
        Node.__init__(self, parent)
        self.is_hover = False

        self.default_color = color
        self.hover_color = Config.purple_500

        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect()
        self.rect.left = shift
        self.paintbar()

        self.handle_mousewheel = self.handle_mousemotion

    def paintbar(self):
        if self.is_hover:
            self.image.fill(self.hover_color)
        else:
            self.image.fill(self.default_color)

    def update(self, state):
        self.paintbar()

    def handle_mousemotion(self, state, event):
        if state.hotbar in state.mouse_int_sprites and \
            state.hotbar.active_mod_index == state.hotbar.BUILDING_SELECTOR and \
                self in state.mouse_int_sprites:
            self.is_hover = True
        elif self.is_hover:
            self.is_hover = False


class BuildingSelector(pygame.sprite.Sprite, Node):

    def __init__(self, parent=None):
        pygame.sprite.Sprite.__init__(self, self.groups)
        Node.__init__(self, parent)
        self.image = pygame.Surface(
            (Config.hotbarwidth, Config.hotbarheight - 20)
        )
        self.paintbar()
        self.rect = self.image.get_rect()
        self.rect.topleft = (10, 10)

        self.options = pygame.sprite.Group()

        size = self.rect.height
        colors = itertools.cycle((Config.red_300, Config.red_700))
        for x in range(round(self.rect.width/size)):
            option = SelectorOption(size, x*size, next(colors), parent=self)
            self.options.add(option)

    def paintbar(self):
        self.image.fill(Config.bluegrey_500)

    def update(self, state):
        self.options.update(state)
        self.options.draw(self.image)

    def handle_mousewheel(self, state, event):
        if state.hotbar in state.mouse_int_sprites and \
                state.hotbar.active_mod_index == state.hotbar.BUILDING_SELECTOR:
            self.rect.center = (
                self.rect.center[0] +
                ((event.x+event.y) * Config.scroll_speed),
                self.rect.center[1]
            )
            state.calculate_mouse_int_sprites()


class InfoBar(pygame.sprite.Sprite, Node):

    def __init__(self, parent=None):
        pygame.sprite.Sprite.__init__(self, self.groups)
        Node.__init__(self, parent)
        self.image = pygame.Surface(
            (Config.hotbarwidth, Config.hotbarheight - 20))
        self.paintbar()
        self.rect = self.image.get_rect()
        self.rect.topleft = (10, 10)

    def paintbar(self):
        self.image.fill(Config.bluegrey_500)

    def update(self, state):
        self.paintbar()

    def handle_mousewheel(self, state, event):
        if state.hotbar in state.mouse_int_sprites and \
            state.hotbar.active_mod_index == state.hotbar.INFOBAR and \
                self in state.mouse_int_sprites:
            pass


class MultiInfoBar(pygame.sprite.Sprite, Node):

    def __init__(self, parent=None):
        pygame.sprite.Sprite.__init__(self, self.groups)
        Node.__init__(self, parent)
        self.image = pygame.Surface(
            (Config.hotbarwidth, Config.hotbarheight - 20))
        self.paintbar()
        self.rect = self.image.get_rect()
        self.rect.topleft = (10, 10)

    def paintbar(self):
        self.image.fill(Config.bluegrey_500)

    def update(self, state):
        self.paintbar()

    def handle_mousewheel(self, state, event):
        if state.hotbar in state.mouse_int_sprites and \
            state.hotbar.active_mod_index == state.hotbar.MULTI_INFOBAR and \
                self in state.mouse_int_sprites:
            pass


class Hotbar(pygame.sprite.Sprite, Node):

    BUILDING_SELECTOR = 0
    INFOBAR = 1
    MULTI_INFOBAR = 2

    DEFAULT_MOD = 0

    def __init__(self, group, parent=None):
        pygame.sprite.Sprite.__init__(self, self.groups)
        Node.__init__(self, parent)
        self.image = pygame.Surface(
            (Config.hotbarwidth, Config.hotbarheight))
        self.paintbar()
        self.rect = self.image.get_rect()
        self.rect.topleft = (
            round(Config.width / 2) - round(Config.hotbarwidth/2),
            Config.height - Config.hotbarheight
        )

        BuildingSelector.groups = group
        InfoBar.groups = group
        MultiInfoBar.groups = group
        SelectorOption.groups = group

        self.building_selector = BuildingSelector(parent=self)
        self.infobar = InfoBar(parent=self)
        self.multi_infobar = MultiInfoBar(parent=self)

        self.mods = (self.building_selector, self.infobar, self.multi_infobar)

        self.active_mod_index = self.DEFAULT_MOD

    @property
    def active_mod(self):
        return self.mods[self.active_mod_index]

    def paintbar(self):
        self.image.fill(Config.dark)

    def update(self, state):
        self.paintbar()
        self.image.blit(self.active_mod.image, self.active_mod.rect.topleft)
        self.active_mod.update(state)

    def handle_mousewheel(self, state, event):
        if self in state.mouse_int_sprites:
            pass
