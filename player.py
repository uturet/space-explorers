import pygame
from options import Options as Opt


class Player(pygame.sprite.Sprite):
    radius = 100

    def __init__(self, pos, color=Opt.blue):
        pygame.sprite.Sprite.__init__(self)
        self.color = color
        size = 30
        rad = size/2
        self.pos = pos
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        pygame.draw.circle(self.image, self.color, (rad, rad), rad)

    def update(self):
        self.rect.x += 5
        if self.rect.left > Opt.width:
            self.rect.right = 0

    def show_area(self, field):
        pygame.draw.circle(field.image, self.color, self.pos, self.radius, 1)
