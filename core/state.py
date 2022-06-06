import pygame
from core.config import Config
from user_interface import Minimap, Background, Mouse, MouseTracker, Hotbar
from game_objects import Transmitter
from core.livecycle_manager import LiveCicleManager
from core.collision_handler import CollisionHandler


class State(LiveCicleManager, CollisionHandler):
    move_bg = set()
    mouse_int_sprites = set()

    def __init__(self):
        self.allgroup = pygame.sprite.Group()
        self.uigroup = pygame.sprite.LayeredUpdates()
        self.bggroup = pygame.sprite.LayeredUpdates()
        self.interactable_group = pygame.sprite.Group()
        self.gamegroup = pygame.sprite.Group()

        self.set_group_attachmet()

        self.screen = pygame.display.set_mode((Config.width, Config.height))
        self.bg = Background()
        self.mouse = Mouse(self.bg)
        self.mouse_tracker = MouseTracker()
        self.hotbar = Hotbar(self.interactable_group)
        self.minimap = Minimap()

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((Config.width, Config.height))

        self.detect_handlers(self.uigroup)
        self.detect_handlers(self.interactable_group)
        self.detect_handlers(self.gamegroup)

    def update(self):
        self.calculate_mouse_int_sprites()

        self.allgroup.update(self)

        self.uigroup.draw(self.screen)
        self.bggroup.draw(self.bg.image)

        for move in self.move_bg:
            move()

    def set_group_attachmet(self):
        Transmitter._layer = 3

        Transmitter.groups = (self.allgroup, self.bggroup, self.gamegroup)

        Background._layer = 1
        MouseTracker._layer = 2
        Minimap._layer = 9
        Hotbar._layer = 9

        MouseTracker.groups = (self.allgroup, self.uigroup)
        Hotbar.groups = (self.allgroup, self.uigroup)
        Background.groups = (self.allgroup, self.uigroup)
        Minimap.groups = (self.allgroup, self.uigroup)
