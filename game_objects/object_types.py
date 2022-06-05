from turtle import pos
import pygame


class Building(pygame.sprite.Sprite):

    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.pos = pos


class Particle(pygame.sprite.Sprite):
    pos = None
    velosity = None
    acceleration = None

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.groups)
