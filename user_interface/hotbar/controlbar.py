from user_interface.hotbar import Hotbar
from user_interface import Node, Button
import pygame
from core.event import HOTBARSELECTMOD
from core.config import Config


class ControlBar(Node):
    info_provider = None

    def __init__(self, parent, width, height, shift):
        self.width = width
        self.height = height
        super().__init__(parent)
        self.rect.left = shift

        self.destroy_button = DestroyButton(self, self.handle_destroy_provider)
        self.image.blit(
            self.destroy_button.image, self.destroy_button.rect)

    def handle_destroy_provider(self):
        pygame.event.post(pygame.event.Event(HOTBARSELECTMOD))


class DestroyButton(Button):
    color = Config.red_500

    def __init__(self, parent, handler):
        super().__init__(parent)
        self.handler = handler
        self.rect.topleft = (0, 0)

    def handle_mousebuttonup(self, state, event):
        if state.hotbar.active_mod_index == Hotbar.INFOMOD and \
                self in state.mouse_intersected:
            self.handler()
