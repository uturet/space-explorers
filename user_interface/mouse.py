from core.config import Config
import pygame


class Mouse(pygame.sprite.Sprite):

    INACTIVE = 0
    SELECT = 1
    PREVIEW = 2

    DEFAULT_MOD = 0
    active_mod = 0

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
        self.active_mod = self.DEFAULT_MOD
        self.image.set_alpha(0)

    def update(self, state):
        pass

    def handle_mousemotion(self, state, event):
        if self.active_mod == self.PREVIEW:
            self.intersections.clear()

            state.grid.rect_intersects(self.bg_rect, self.intersections)

            self.preview.handle_intersections(state, self.intersections)
            self.image.fill((255, 255, 255, 0))
            self.preview.update_preview_image()

            self.image.blit(self.preview.preview_image, (0, 0))
        elif self.active_mod == self.SELECT:
            pass

    def handle_mousebuttondown(self, state, event):
        if event.button != 1:
            return
        if self.active_mod == self.DEFAULT_MOD:
            self.active_mod = self.SELECT
        elif self.active_mod == self.SELECT:
            pass

    def handle_mousebuttonup(self, state, event):
        if event.button != 1:
            return
        if self.active_mod == self.SELECT:
            pass
