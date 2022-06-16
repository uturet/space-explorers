import pygame
from core.config import Config


class InfoManager:
    width = 20
    height = 4

    def __init__(self):
        self.bg_color = (*Config.bluegrey_500, 100)
        self.h_frames = []
        self.e_frames = []
        self.create_frames(self.h_frames, Config.green_500)
        self.create_frames(self.e_frames, Config.blue_500)

    def create_frames(self, frames, color):
        for i in range(0, 11):
            image = pygame.Surface(
                (self.width, self.height), pygame.SRCALPHA)
            inner_image = pygame.Surface(
                (i*(self.width/10), self.height), pygame.SRCALPHA)
            image.fill(self.bg_color)
            inner_image.fill(color)
            image.blit(inner_image, (0, 0))
            converted = image.convert_alpha()
            frames.append(converted)
