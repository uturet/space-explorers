from game_objects.object_type import Building
from user_interface.hotbar import ControlBar
from user_interface import Node
from game_objects.buildings import building_previews
from core import collision_handler as ch
from core.config import Config
import pygame
import math


class MultiInfoBar(Node):
    width = Config.hotbarwidth
    height = Config.hotbarheight

    def __init__(self, parent):
        super().__init__(parent)
        self. info_providers = set()
        self._previews = set()
        self.infobar_preview = None
        self.control_bar = ControlBar(
            self, self.width,
            self.height, MultiInfobarPreview.width)

    def set_info_providers(self, sprites):
        self.info_providers = sprites
        [spr.set_ui_type(Building.SELECTED) for spr in sprites]
        for p in self._previews:
            p.kill()
        self._previews.clear()
        x_shift = round(MultiInfobarPreview.width /
                        MultiInfobarPreviewOption.width)

        self.infobar_preview = MultiInfobarPreview(self, math.ceil(
            len(sprites)/x_shift) * MultiInfobarPreviewOption.height)

        for i, sprite in enumerate(sprites):
            p = MultiInfobarPreviewOption(self)
            self._previews.add(p)
            building_previews[sprite.__class__.__name__]\
                .draw_small_option_image(p.rect.center, p.image)
            p.rect.left = (i % x_shift) * p.rect.w
            p.rect.top = min(math.floor(i/x_shift),
                             math.ceil(i/x_shift)) * p.rect.h
            self.infobar_preview.image.blit(p.image, p.rect)

        self.image.blit(self.infobar_preview.image, self.infobar_preview.rect)
        self.image.blit(self.control_bar.image, self.control_bar.rect)


class MultiInfobarPreview(Node):
    width = 200
    height = MultiInfoBar.height
    color = Config.black

    def __init__(self, parent, height):
        self.height = max(self.height, height)
        super().__init__(parent)
        self.image.fill(self.color)


class MultiInfobarPreviewOption(Node):
    width = 50
    height = 50
