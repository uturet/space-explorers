import pygame
from core.config import Config


class Background(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.dimens = (Config.bigmapwidth, Config.bigmapheight)
        self.image = pygame.Surface(self.dimens)
        self.paintbg()
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)

    def paintbg(self):
        self.image.fill(Config.bg)

    def update(self, state):
        pass

    @property
    def pos(self):
        return self.rect.center

    def handle_mousemotion(self, state, event):
        state.move_bg.clear()
        if Config.width*Config.move_area > event.pos[0]:
            state.move_bg.add(self.move_left)
        if (Config.width - Config.width*Config.move_area) < event.pos[0]:
            state.move_bg.add(self.move_right)
        if Config.height*Config.move_area > event.pos[1]:
            state.move_bg.add(self.move_top)
        if (Config.height - Config.height*Config.move_area) < event.pos[1]:
            state.move_bg.add(self.move_bot)

    def move_left(self):
        self.rect.center = (
            min(round(self.dimens[0]/2), self.rect.center[0] + Config.speed),
            self.rect.center[1]
        )

    def move_right(self):
        self.rect.center = (
            max(Config.width - round(self.dimens[0]/2),
                self.rect.center[0] - Config.speed),
            self.rect.center[1]
        )

    def move_top(self):
        self.rect.center = (
            self.rect.center[0],
            min(round(self.dimens[1]/2), self.rect.center[1] + Config.speed)
        )

    def move_bot(self):
        self.rect.center = (
            self.rect.center[0],
            max(Config.height - round(self.dimens[1]/2),
                self.rect.center[1] - Config.speed)
        )

    def move(self, x, y):
        x = -(x - round(self.dimens[0]/2) - round(Config.width/2))
        y = -(y - round(self.dimens[1]/2) - round(Config.height/2))

        x = min(
            round(self.dimens[0]/2),
            max(Config.width - round(self.dimens[0]/2),
                x)
        )

        y = min(
            round(self.dimens[1]/2),
            max(Config.height - round(self.dimens[1]/2),
                y)
        )

        self.rect.center = (x, y)
