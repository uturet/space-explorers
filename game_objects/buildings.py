import pygame
from game_objects.object_types import Building
from config import Config


class Transmitter(Building):
    coverage_radius = 100
    size = 20
    radius = 10
    color = Config.blue_500

    option_radius = 40

    def __init__(self, pos):
        super().__init__(pos)

    @classmethod
    def get_option_image(cls):
        image = pygame.Surface(
            (Config.building_selector_height, Config.building_selector_height),
            pygame.SRCALPHA)
        rect = image.get_rect()
        pygame.draw.circle(image, cls.color, rect.center, cls.option_radius)

        return image


buildings = (
    Transmitter,
)
