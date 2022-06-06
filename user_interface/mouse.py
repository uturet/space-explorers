from core.config import Config
import pygame
from core import collision_handler as ch


class Mouse:
    pos = (Config.width/2, Config.height/2)

    def __init__(self, bg):
        self._bg = bg

    @property
    def pos_x(self):
        x = round(
            self.pos[0] - (self._bg.pos[0] - (self._bg.dimens[0]/2)))
        return max(0, min(x, self._bg.dimens[0]))

    @property
    def pos_y(self):
        y = round(
            self.pos[1] - (self._bg.pos[1] - (self._bg.dimens[1]/2)))
        return max(0, min(y, self._bg.dimens[1]))

    def bg_pos_to_abs(self, pos):
        x = round(
            pos[0] + (self._bg.pos[0] - (self._bg.dimens[0]/2)))

        y = round(
            pos[1] + (self._bg.pos[1] - (self._bg.dimens[1]/2)))
        return x, y

    @property
    def bg_pos(self):
        return (self.pos_x, self.pos_y)


class MouseTracker(pygame.sprite.Sprite):

    is_active = False
    preview = None
    preview_rect = None
    groups = ()
    collisions = set()
    sprite_type = None

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.dimens = (Config.mouse_tracker_width, Config.mouse_tracker_height)
        self.image = pygame.Surface(self.dimens, pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)

    def set_preview(self, preview, pos):
        self.is_active = True
        self.image = pygame.Surface(
            (preview.cover_size, preview.cover_size), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.bg_rect = self.rect.copy()
        self.rect.center = pos

        self.preview = preview
        self.preview_rect = preview.preview_image.get_rect()
        self.preview.update_preview_image()
        self.image.blit(self.preview.preview_image, (0, 0))

    def clear_preview(self):
        self.is_active = False
        self.image.set_alpha(0)

    def update(self, state):
        pass

    def handle_mousemotion(self, state, event):
        if self.is_active:
            self.rect.center = event.pos
            self.bg_rect.center = state.mouse.bg_pos
            self.collisions.clear()
            ch.rect_collides(self.bg_rect, state.gamegroup, self.collisions)
            self.preview.handle_collisions(state, self.collisions)
            self.image.fill((255, 255, 255, 0))
            self.preview.update_preview_image()
            self.image.blit(self.preview.preview_image, (0, 0))
