from core.config import Config
import pygame
from core.event import MOUSEPRESELECT, MOUSESELECT, MOUSEENDSELECT
from core import collision_handler as ch


class Mouse(pygame.sprite.Sprite):

    INACTIVE = 0
    SELECT = 1
    PREVIEW = 2

    active_mod = INACTIVE
    select_point = (0, 0)
    pos = (0, 0)
    groups = ()

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.preview_image = pygame.Surface(
            (Config.preview_cover_size,
             Config.preview_cover_size), pygame.SRCALPHA)
        self.preview_rect = self.preview_image.get_rect()
        self.selector_image = pygame.Surface(
            (Config.width, Config.height), pygame.SRCALPHA)
        self.selector_rect = self.selector_image.get_rect()
        self.image = self.preview_image
        self.rect = self.preview_rect
        self.bg_rect = self.rect.copy()

    def set_mod(self, mod_index):
        if mod_index == self.INACTIVE:
            self.active_mod = self.INACTIVE
        elif mod_index == self.SELECT:
            self.active_mod = self.SELECT
            self.image = self.selector_image
            self.rect = self.selector_rect
            self.bg_rect = self.rect.copy()
        elif mod_index == self.PREVIEW:
            self.active_mod = self.PREVIEW
            self.image = self.preview_image
            self.rect = self.preview_rect
            self.bg_rect = self.rect.copy()
        self.image.fill((255, 255, 255, 0))

    def handle_mousemotion(self, state, event):
        self.pos = event.pos
        if self.active_mod == self.PREVIEW:
            self.image.fill((255, 255, 255, 0))
            self.rect.center = self.pos
            self.bg_rect.center = state.bg.abs_pos_to_bg(*event.pos)
        elif self.active_mod == self.SELECT:
            self.image.fill((255, 255, 255, 0))
            abs_rect = ch.rect_from_points(
                state.bg.bg_pos_to_abs(*self.select_point), event.pos)
            pygame.draw.rect(
                self.image, Config.yellow_500,
                abs_rect, 2)

    def handle_mousebuttondown(self, state, event):
        if event.button != 1:
            return
        if self.active_mod == self.INACTIVE and \
            state.minimap not in state.mouse_intersected and \
                state.hotbar not in state.mouse_intersected:
            self.set_mod(self.SELECT)
            self.select_point = state.bg.abs_pos_to_bg(
                event.pos[0], event.pos[1])
            pygame.event.post(pygame.event.Event(MOUSEPRESELECT))

    def handle_mousebuttonup(self, state, event):
        if event.button != 1:
            return
        if self.active_mod == self.SELECT:
            self.set_mod(self.INACTIVE)
            self.image.fill((255, 255, 255, 0))
            bg_rect = ch.rect_from_points(
                self.select_point, state.bg.abs_pos_to_bg(*event.pos))
            pygame.event.post(pygame.event.Event(
                MOUSEENDSELECT, {'rect': bg_rect}))
