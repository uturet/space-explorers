from user_interface.hotbar.hotbar import Hotbar, HotbarMod
from game_objects.buildings import building_previews
from core import collision_handler as ch
from user_interface.node import Node
from core.config import Config
import pygame


class InfoBar(HotbarMod):
    hotbar_mod = Hotbar.INFOBAR
    info_provider = None

    def __init__(self, parent=None):
        super().__init__(parent)

    def set_info_provider(self, sprite):
        self.info_provider = sprite
