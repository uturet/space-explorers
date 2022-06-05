import pygame
from config import Config


class Hotbar(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface(
            (Config.hotbarwidth, Config.hotbarheight))
        self.paintbar()
        self.rect = self.image.get_rect()
        self.rect.midbottom = (round(Config.width / 2), Config.height)

    def paintbar(self):
        self.image.fill(Config.dark)

    def update(self, state):
        self.paintbar()
