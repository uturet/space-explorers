import pygame
from game_objects.object_type import Building, Preview
from core.config import Config
from core.property import EnergyInteraction


class Transmitter(Building):
    width = 20
    height = width
    radius = width/2
    color = Config.blue_500

    def draw_frame(self, image, color):
        pygame.draw.circle(image, color,
                           (self.radius, self.radius), self.radius)


class TransmitterPreview(Preview):
    building = Transmitter
    preview_color = Config.blue_200

    def draw_frame(self, image, color):
        pygame.draw.circle(image, color,
                           self.rect.center, self.radius)

    def draw_option_image(self, rect, image):
        pygame.draw.circle(image, self.color,
                           rect.center, self.option_radius)

    def draw_small_option_image(self, rect, image):
        pygame.draw.circle(image, self.color, rect.center,
                           self.small_option_radius)


class Generator(Building):

    width = 40
    height = width
    radius = width/2
    color = Config.green_500

    def draw_frame(self, image, color):
        pygame.draw.circle(image, color,
                           (self.radius, self.radius), self.radius)


class GeneratorPreview(Preview):
    building = Generator
    preview_color = Config.blue_200

    def draw_frame(self, image, color):
        pygame.draw.circle(image, color,
                           self.rect.center, self.radius)

    def draw_option_image(self, rect, image):
        pygame.draw.circle(image, self.color,
                           rect.center, self.option_radius)

    def draw_small_option_image(self, rect, image):
        pygame.draw.circle(image, self.color, rect.center,
                           self.small_option_radius)


building_previews = {}
