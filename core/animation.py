from collections import namedtuple
import pygame

Frame = namedtuple('Frame', 'image rect mask')


class ColorFrameList:
    def __init__(self):
        self.height = 0
        self.width = 0
        self.colors = ()
        self.frames = []

    def select_frame(self, i, attr='frames'):
        self.image = getattr(self, attr)[i].image
        self.rect = getattr(self, attr)[i].rect
        self.mask = getattr(self, attr)[i].mask

    def create_frames(self, attr='frames', center=None):
        self.frames = []
        for color in self.colors:
            image = pygame.Surface(
                (self.width, self.height), pygame.SRCALPHA)
            self.rect = image.get_rect()
            if center:
                self.rect.center = center
            self.draw_frame(image, color)
            converted = image.convert_alpha()
            getattr(self, attr).append(Frame(
                converted, self.rect, pygame.mask.from_surface(converted)))

    def draw_frame(self, image, color):
        raise NotImplementedError()
