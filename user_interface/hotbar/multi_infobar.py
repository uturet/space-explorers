from user_interface.hotbar.hotbar import Hotbar, HotbarMod
from game_objects.buildings import building_previews
from core import collision_handler as ch
from user_interface.node import Node
from core.config import Config
import itertools
import pygame


class MultiInfoBar(HotbarMod):
    hotbar_mod = Hotbar.MULTI_INFOMOD
    info_providers = set()

    def __init__(self, parent=None):
        super().__init__(parent)

    def set_info_providers(self, sprites):
        self.info_providers = sprites
