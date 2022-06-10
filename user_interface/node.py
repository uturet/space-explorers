import pygame
from collections import namedtuple
Coords = namedtuple('Coords', 'left top right bottom')


class Node(pygame.sprite.Sprite):

    def __init__(self, parent=None):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.parent = parent

        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)

    def calculate_abs_coords(self, parent=None, coords=None):
        enter = False
        if not coords:
            enter = True
            parent = self.parent
            coords = {
                'left': self.rect.left,
                'top': self.rect.top,
                'right': self.rect.right,
                'bottom': self.rect.bottom,
            }

        if parent:
            coords['left'] += parent.rect.left
            coords['top'] += parent.rect.top
            coords['right'] += parent.rect.left
            coords['bottom'] += parent.rect.top
            if hasattr(parent, 'parent'):
                self.calculate_abs_coords(parent.parent, coords)
        if enter:
            return Coords(**coords)
