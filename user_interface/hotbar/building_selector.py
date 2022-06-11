from user_interface.hotbar import Hotbar, HotbarMod
from user_interface import Node
from game_objects.buildings import building_previews
from core import collision_handler as ch
from core.config import Config
import itertools
import pygame


class Selectbar(HotbarMod):
    selected_option = None

    def __init__(self, parent=None):
        super().__init__(parent)

        self.width = Config.hotbarheight * len(building_previews)
        if self.width < Config.hotbarwidth:
            self.width = Config.hotbarwidth

        self.options = pygame.sprite.Group()

        colors = itertools.cycle((Config.red_300, Config.red_700))
        for x, preview in enumerate(building_previews.values()):
            option = SelectorOption(
                preview, x*Config.hotbarheight,
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
                state.hotbar.active_mod_index == Hotbar.SELECTMOD):
            self.rect.center = (
                self.rect.center[0] +
                ((event.x+event.y) * Config.scroll_speed),
                self.rect.center[1]
            )

            state.mouse_intersected.difference_update(self.options)
            ch.get_rect_intersect_sprites_by_pos(
                state.mouse.rect.center,
                self.options,
                state.mouse_intersected
            )


class SelectorOption(Node):
    is_hover = False
    is_active = False

    width = Config.hotbarheight
    height = Config.hotbarheight

    def __init__(self, preview, shift, color, parent=None):
        Node.__init__(self, parent)
        self.default_color = color
        self.hover_color = Config.purple_500
        self.active_color = Config.blue_500

        self.preview = preview
        self.rect.left = shift
        self.paintbar()

        self.handle_mousewheel = self.handle_mousemotion

    def paintbar(self):
        if self.is_hover:
            self.image.fill(self.hover_color)
        else:
            self.image.fill(self.default_color)
        if self.is_active:
            pygame.draw.rect(self.image, self.active_color, self.rect, 4)
        self.preview.draw_option_image(self.rect)
        self.image.blit(self.preview.option_image, (0, 0))

    def update(self, state):
        pass

    def handle_mousemotion(self, state, event):
        if (state.hotbar in state.mouse_intersected and
            state.hotbar.active_mod_index == Hotbar.SELECTMOD and
                self in state.mouse_intersected):
            self.is_hover = True
            self.paintbar()
        elif self.is_hover:
            self.is_hover = False
            self.paintbar()

    def handle_mousebuttonup(self, state, event):
        if state.hotbar.active_mod_index != Hotbar.SELECTMOD:
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
                state.grid.add_item(self.preview.building(
                    self.preview.lines.copy(),
                    state.mouse.bg_rect.center))

        if event.button == 3:
            if (self.is_active and
                    state.minimap not in state.mouse_intersected):
                state.hotbar.active_mod.set_selected_option(state)

    def activate(self, state):
        self.is_active = True
        state.mouse.set_preview(self.preview)
        self.paintbar()

    def deactivate(self, state):
        self.is_active = False
        state.mouse.clear_preview()
        self.paintbar()
