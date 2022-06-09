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

    preview = None
    preview_rect = None
    groups = ()
    intersections = set()

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.dimens = (Config.mouse_tracker_width, Config.mouse_tracker_height)
        self.image = pygame.Surface(self.dimens, pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)
        self.bg_rect = self.rect.copy()

    def set_preview(self, preview):
        self.active_mod = self.PREVIEW
        self.image = pygame.Surface(
            (preview.cover_size, preview.cover_size), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.bg_rect = self.rect.copy()

        self.preview = preview
        self.preview_rect = preview.preview_image.get_rect()
        self.preview.update_preview_image()
        self.image.blit(self.preview.preview_image, self.rect.bottomright)

    def clear_preview(self):
        self.active_mod = self.INACTIVE
        self.image.set_alpha(0)

    def update(self, state):
        pass

    def set_selector(self, pos):
        self.image = pygame.Surface(
            (Config.width, Config.height), pygame.SRCALPHA)
        self.rect = self.image.get_rect()

    def clear_selector(self):
        pass

    def handle_mousemotion(self, state, event):
        self.pos = event.pos
        if self.active_mod == self.PREVIEW:
            self.rect.center = self.pos
            self.bg_rect.center = state.bg.abs_pos_to_bg(
                event.pos[0], event.pos[1])
            self.intersections.clear()
            state.grid.rect_intersects(self.bg_rect, self.intersections)

            self.preview.handle_intersections(state, self.intersections)
            self.image.fill((255, 255, 255, 0))
            self.preview.update_preview_image()

            self.image.blit(self.preview.preview_image, (0, 0))
        elif self.active_mod == self.SELECT:
            self.image.fill((255, 255, 255, 0))
            bg_rect = ch.rect_from_points(
                self.select_point, state.bg.abs_pos_to_bg(*event.pos))
            abs_rect = ch.rect_from_points(
                state.bg.bg_pos_to_abs(*self.select_point), event.pos)
            pygame.draw.rect(
                self.image, Config.yellow_500,
                abs_rect, 2)

            pygame.event.post(pygame.event.Event(
                MOUSESELECT, {'rect': bg_rect}))

    def handle_mousebuttondown(self, state, event):
        if event.button != 1:
            return
        if self.active_mod == self.INACTIVE and \
            state.minimap not in state.mouse_intersected and \
                state.hotbar not in state.mouse_intersected:
            self.active_mod = self.SELECT
            self.select_point = state.bg.abs_pos_to_bg(
                event.pos[0], event.pos[1])
            self.set_selector(event.pos)
            pygame.event.post(pygame.event.Event(MOUSEPRESELECT))

    def handle_mousebuttonup(self, state, event):
        if event.button != 1:
            return
        if self.active_mod == self.SELECT:
            self.active_mod = self.INACTIVE
            self.image.fill((255, 255, 255, 0))
            pygame.event.post(pygame.event.Event(MOUSEENDSELECT))
