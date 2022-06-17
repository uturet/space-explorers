import pygame
from core.config import Config


class Minimap(pygame.sprite.Sprite):
    follow_mouse = False

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface(
            (Config.minimapwidth, Config.minimapheight))
        self.paintmap()
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (0, Config.height)
        self.factorx = Config.minimapwidth * 1.0 / Config.bigmapwidth
        self.factory = Config.minimapheight * 1.0 / Config.bigmapheight

    def paintmap(self):
        self.image.fill(Config.dark)
        pygame.draw.rect(
            self.image,
            (150, 0, 0),
            (0, 0, Config.minimapwidth, Config.minimapheight),
            1
        )

    def update(self, state):
        self.paintmap()

        for pl in state.gamegroup:
            pygame.draw.circle(self.image, pl.color,
                               (int(pl.rect.centerx * self.factorx),
                                int(pl.rect.centery * self.factory)
                                ), int(pl.rect.width/20))

        pygame.draw.rect(self.image, (255, 255, 255), (
            round(-state.bg.rect.left * self.factorx, 0),
            round(-state.bg.rect.top * self.factory, 0),
            round(Config.width * self.factorx, 0),
            round(Config.height * self.factory, 0)), 1)

    def handle_mousebuttondown(self, state, event):
        if event.button == 1 and self in state.mouse_intersected:
            self.follow_mouse = True
            x = round(event.pos[0] / self.factorx)
            y = round((event.pos[1] - self.rect.top) / self.factory)
            state.bg.move(x, y)

    def handle_mousebuttonup(self, state, event):
        self.follow_mouse = False

    def handle_mousemotion(self, state, event):
        if self.follow_mouse and self in state.mouse_intersected:
            x = round(event.pos[0] / self.factorx)
            y = round((event.pos[1] - self.rect.top) / self.factory)
            state.bg.move(x, y)
