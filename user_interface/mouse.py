from config import Config
import pygame


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

    @property
    def bg_pos(self):
        return (self.pos_x, self.pos_y)


class MouseTracker(pygame.sprite.Sprite):

    is_active = False
    preview = None
    preview_rect = None
    groups = ()

    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.dimens = (Config.mouse_tracker_width, Config.mouse_tracker_height)
        self._image = pygame.Surface(self.dimens, pygame.SRCALPHA)
        self.rect = self._image.get_rect()
        self.rect.topleft = (0, 0)
        self.image = self._image.convert_alpha()

    def set_preview(self, preview, pos):
        self.is_active = True
        self.rect.center = pos
        self.preview = preview
        self.preview_rect = preview.get_rect()
        self._image.blit(preview, (0, 0))
        self.image = self._image.convert_alpha()

    def clear_preview(self):
        self.is_active = False
        self.image.set_alpha(0)

    def update(self, state):
        pass

    def handle_mousemotion(self, state, event):
        if self.is_active:
            self.rect.center = event.pos
