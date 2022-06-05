import pygame
from config import Config


class Radarmap(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface(
            (Config.radarmapwidth, Config.radarmapheight))
        self.paintmap()
        self.rect = self.image.get_rect()
        self.rect.topleft = (Config.width - Config.radarmapwidth, 0)
        self.factorx = Config.radarmapwidth * 1.0 / Config.bigmapwidth
        self.factory = Config.radarmapheight * 1.0 / Config.bigmapheight

    def paintmap(self):
        self.image.fill(Config.dark)
        pygame.draw.rect(
            self.image,
            (150, 0, 0),
            (0, 0, Config.radarmapwidth, Config.radarmapheight),
            1
        )

    def update(self, state):
        self.paintmap()

        for pl in state.bggroup:
            pygame.draw.circle(self.image, pl.color,
                               (int(pl.pos[0] * self.factorx),
                                int(pl.pos[1] * self.factory)
                                ), 2)

        pygame.draw.rect(self.image, (255, 255, 255), (
            round(-state.bg.rect.left * self.factorx, 0),
            round(-state.bg.rect.top * self.factory, 0),
            round(Config.width * self.factorx, 0),
            round(Config.height * self.factory, 0)), 1)
