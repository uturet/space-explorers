from user_interface import Node
from game_objects.buildings import building_previews
from core import collision_handler as ch
from core.config import Config
from core.animation import ColorFrameList
import itertools
import pygame


class Selectbar(Node):
    width = Config.hotbarwidth
    height = Config.hotbarheight
    _selected_option = None

    def __init__(self,):
        super().__init__()

        self.width = Config.hotbarheight * len(building_previews)
        if self.width < Config.hotbarwidth:
            self.width = Config.hotbarwidth

        self.options = pygame.sprite.Group()

        colors = itertools.cycle((Config.red_300, Config.red_700))
        for x, preview in enumerate(building_previews.values()):
            option = SelectorOption(
                preview, x*Config.hotbarheight,
                next(colors)
            )
            self.options.add(option)

    @property
    def selected_option(self):
        return self._selected_option

    @selected_option.setter
    def selected_option(self, option):
        if option:
            option.set_type(SelectorOption.SELECTED)
        if self._selected_option:
            self._selected_option.set_type(SelectorOption.DEFAULT)
        self._selected_option = option

    def update(self, state):
        self.options.update(state)

    def handle_mousewheel(self, state, event):
        if (state.hotbar in state.mouse_intersected):
            self.rect.center = (
                self.rect.center[0] +
                ((event.x+event.y) * Config.scroll_speed),
                self.rect.center[1])

    def handle_mousemotion(self, state, event):
        if self.selected_option:
            self.selected_option.preview.handle_mousemotion(state, event)

    def handle_mousebuttonup(self, state, event):
        if event.button == 1:
            if (state.hotbar not in state.mouse_intersected):
                if (self.selected_option and
                    self.selected_option.preview.valid and
                        state.minimap not in state.mouse_intersected):
                    state.create_selected_building(
                        self.selected_option.preview)
            else:
                for option in self.options:
                    pos = (event.pos[0]-self.rect.left,
                           event.pos[1]-self.rect.top)
                    if not ch.is_pos_intersects_rect(pos, option.rect):
                        continue
                    if option.type == SelectorOption.SELECTED:
                        self.selected_option = None
                    else:
                        state.mouse.set_mod(state.mouse.PREVIEW)
                        self.selected_option = option
                    break

        if event.button == 3:
            if (state.minimap not in state.mouse_intersected):
                self.selected_option = None
                state.mouse.set_mod(state.mouse.INACTIVE)
                state.tmp_preview_group.clear()

    def draw(self):
        self.options.draw(self.image)


class SelectorOption(pygame.sprite.Sprite, ColorFrameList):
    DEFAULT = 0
    SELECTED = 1
    type = DEFAULT

    width = Config.hotbarheight
    height = Config.hotbarheight

    def __init__(self, preview, shift, color):
        pygame.sprite.Sprite.__init__(self)
        self.preview = preview
        self.colors = (color, Config.blue_500)
        self.create_frames(left=shift)
        self.select_frame(self.type)

    def set_type(self, index):
        self.type = index
        self.select_frame(index)

    def update(self, state):
        pass

    def draw_frame(self, image, color, index):
        if index == self.DEFAULT:
            image.fill(color)
        elif index == self.SELECTED:
            pygame.draw.rect(image, color,
                             (0, 0, self.width, self.height), 4)
        self.preview.draw_option_image(
            (self.width/2, self.height/2), image)
