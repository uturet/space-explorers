from user_interface.hotbar.hotbar import Hotbar, HotbarMod
from game_objects.buildings import building_previews
from core import collision_handler as ch
from user_interface.node import Node
from core.config import Config
import pygame
from core.event import HOTBARSELECTMOD


class InfoBar(HotbarMod):
    hotbar_mod = Hotbar.INFOMOD

    def __init__(self, parent):
        super().__init__(parent)
        self.infobar_preview = InfobarPreview(self)
        self.control_bar = ControlBar(self)

    def set_info_provider(self, sprite):
        self.control_bar.info_provider = sprite
        building_previews[sprite.__class__.__name__].draw_option_image(
            self.infobar_preview.image, self.infobar_preview.rect)
        self.image.blit(self.infobar_preview.image, self.infobar_preview.rect)
        self.image.blit(self.control_bar.image, self.control_bar.rect)


class InfobarPreview(Node):
    width = InfoBar.height
    height = InfoBar.height


class ControlBar(Node):
    width = InfoBar.width
    height = InfoBar.height
    info_provider = None

    def __init__(self, parent):
        super().__init__(parent)
        self.rect.left = InfobarPreview.width

        self.destroy_button = DestroyButton(self, self.handle_destroy_provider)
        self.image.blit(
            self.destroy_button.image, self.destroy_button.rect)

    def handle_destroy_provider(self):
        pygame.event.post(pygame.event.Event(HOTBARSELECTMOD))


class Button(Node):
    width = 50
    height = 50
    color = Config.blue_500

    def __init__(self, parent):
        Node.__init__(self, parent)
        self.rect.topleft = (0, 0)
        self.paintbtn()

    def paintbtn(self):
        self.image.fill(self.color)


class DestroyButton(Button):
    color = Config.red_500

    def __init__(self, parent, handler):
        super().__init__(parent)
        self.handler = handler
        self.rect.topleft = (0, 0)

    def handle_mousebuttonup(self, state, event):
        if state.hotbar.active_mod_index == InfoBar.hotbar_mod and \
                self in state.mouse_intersected:
            self.handler()
