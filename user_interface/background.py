import pygame
from core.config import Config


class Background(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.moves = set()
        self.dimens = (Config.bigmapwidth, Config.bigmapheight)
        self.image = pygame.Surface(self.dimens)
        self.rect = self.image.get_rect()
        self.box = self.rect.copy()
        self.rect.topleft = (0, 0)
        self.abs_rect = pygame.Rect(0, 0, Config.width, Config.height)

    def paintbg(self):
        self.image.fill((255, 255, 255))

    def update(self, state):
        for move in self.moves:
            move()
        if self.moves:
            self.abs_rect.left = -self.rect.left
            self.abs_rect.top = -self.rect.top
        # self.image.fill((255, 255, 255, 0))

    @property
    def pos(self):
        return self.rect.center

    def handle_mousemotion(self, state, event):
        self.moves.clear()
        if Config.width*Config.move_area > event.pos[0]:
            self.moves.add(self.move_left)
        if (Config.width - Config.width*Config.move_area) < event.pos[0]:
            self.moves.add(self.move_right)
        if Config.height*Config.move_area > event.pos[1]:
            self.moves.add(self.move_top)
        if (Config.height - Config.height*Config.move_area) < event.pos[1]:
            self.moves.add(self.move_bot)

    def move_left(self):
        self.rect.right = min(Config.bigmapwidth,
                              self.rect.right + Config.speed)

    def move_right(self):
        self.rect.left = max(Config.width-Config.bigmapwidth,
                             self.rect.left - Config.speed)

    def move_top(self):
        self.rect.bottom = min(Config.bigmapheight,
                               self.rect.bottom + Config.speed)

    def move_bot(self):
        self.rect.top = max(Config.height-Config.bigmapheight,
                            self.rect.top - Config.speed)

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
        self.abs_rect.topleft = self.rect.topleft

    def bg_pos_to_abs(self, x, y):
        x = round(x + (self.rect.centerx - (self.dimens[0]/2)))
        y = round(y + (self.rect.centery - (self.dimens[1]/2)))
        return x, y

    def abs_pos_to_bg(self, x, y):
        x = round(x - (self.rect.centerx - (self.dimens[0]/2)))
        x = max(0, min(x, self.dimens[0]))
        y = round(y - (self.rect.centery - (self.dimens[1]/2)))
        y = max(0, min(y, self.dimens[1]))
        return x, y
