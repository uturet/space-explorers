import pygame
from core.config import Config
import itertools
from user_interface.node import Node
from game_objects.buildings import building_previews
from core import collision_handler as ch


class SelectorOption(pygame.sprite.Sprite, Node):
    is_hover = False
    is_active = False

    def __init__(self, preview, shift, color, parent=None):
        pygame.sprite.Sprite.__init__(self, self.groups)
        Node.__init__(self, parent)
        self.hotbar_mod = Hotbar.BUILDING_SELECTOR

        self.default_color = color
        self.hover_color = Config.purple_500
        self.active_color = Config.blue_500

        self.preview = preview

        self.image = pygame.Surface(
            (Config.building_selector_height, Config.building_selector_height))
        self.rect = self.image.get_rect()
        self.rect.left = shift
        self.paintbar()

        self.handle_mousewheel = self.handle_mousemotion

    def paintbar(self):
        if self.is_hover:
            self.image.fill(self.hover_color)
        else:
            self.image.fill(self.default_color)
        self.image.blit(self.preview.option_image, (0, 0))
        if self.is_active:
            pygame.draw.rect(self.image, self.active_color, self.rect, 4)

    def update(self, state):
        pass

    def handle_mousemotion(self, state, event):
        if (state.hotbar in state.mouse_intersected and
            state.hotbar.active_mod_index == self.hotbar_mod and
                self in state.mouse_intersected):
            self.is_hover = True
            self.paintbar()
        elif self.is_hover:
            self.is_hover = False
            self.paintbar()

    def handle_mousebuttonup(self, state, event):
        if state.hotbar.active_mod_index != self.hotbar_mod:
            return
        if event.button == 1:
            if (state.hotbar in state.mouse_intersected and
                    self in state.mouse_intersected):
                if self.is_active:
                    state.hotbar.active_mod.set_selected_option(state)
                else:
                    state.hotbar.active_mod.set_selected_option(state, self)
            elif (self.is_active and
                    state.minimap not in state.mouse_intersected and
                    state.hotbar not in state.mouse_intersected):
                state.create_gameobj(self.preview.building, state.mouse.bg_pos)
        if event.button == 3:
            if (self.is_active and
                    state.minimap not in state.mouse_intersected):
                state.hotbar.active_mod.set_selected_option(state)

    def activate(self, state):
        self.is_active = True
        state.mouse_tracker.set_preview(
            self.preview,
            state.mouse.pos
        )
        self.paintbar()

    def deactivate(self, state):
        self.is_active = False
        state.mouse_tracker.clear_preview()
        self.paintbar()


class BuildingSelector(pygame.sprite.Sprite, Node):

    selected_option = None

    def __init__(self, parent=None):
        pygame.sprite.Sprite.__init__(self, self.groups)
        Node.__init__(self, parent)
        self.hotbar_mod = Hotbar.BUILDING_SELECTOR

        width = Config.building_selector_height * len(building_previews)
        if width < Config.building_selector_width:
            width = Config.building_selector_width
        self.image = pygame.Surface(
            (width, Config.building_selector_height))
        self.paintbar()
        self.rect = self.image.get_rect()
        self.rect.topleft = (10, 10)

        self.options = pygame.sprite.Group()

        colors = itertools.cycle((Config.red_300, Config.red_700))
        for x, preview in enumerate(building_previews):
            option = SelectorOption(
                preview(), x*Config.building_selector_height,
                next(colors),
                parent=self
            )
            self.options.add(option)

    def set_selected_option(self, state, option=None):
        if self.selected_option:
            self.selected_option.deactivate(state)
            self.selected_option = None
        if option:
            self.selected_option = option
            option.activate(state)

    def paintbar(self):
        self.image.fill(Config.bluegrey_500)

    def update(self, state):
        self.options.update(state)
        self.options.draw(self.image)

    def handle_mousewheel(self, state, event):
        if (state.hotbar in state.mouse_intersected and
                state.hotbar.active_mod_index == self.hotbar_mod):
            self.rect.center = (
                self.rect.center[0] +
                ((event.x+event.y) * Config.scroll_speed),
                self.rect.center[1]
            )

            state.mouse_intersected.difference_update(self.options)
            ch.get_rect_intersect_sprites_by_pos(
                state.mouse.pos,
                self.options,
                state.mouse_intersected
            )


class InfoBar(pygame.sprite.Sprite, Node):

    def __init__(self, parent=None):
        pygame.sprite.Sprite.__init__(self, self.groups)
        Node.__init__(self, parent)
        self.hotbar_mod = Hotbar.INFOBAR

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
        if (state.hotbar in state.mouse_intersected and
            state.hotbar.active_mod_index == self.hotbar_mod and
                self in state.mouse_intersected):
            pass


class MultiInfoBar(pygame.sprite.Sprite, Node):

    def __init__(self, parent=None):
        pygame.sprite.Sprite.__init__(self, self.groups)
        Node.__init__(self, parent)
        self.hotbar_mod = Hotbar.MULTI_INFOBAR

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
        if (state.hotbar in state.mouse_intersected and
            state.hotbar.active_mod_index == self.hotbar_mod and
                self in state.mouse_intersected):
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
        if self in state.mouse_intersected:
            pass
