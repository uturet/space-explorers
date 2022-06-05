import pygame
from object_types import Building
from config import Config


class Transmitter(Building):
    coverage_radius = 100
    size = 20
    radius = 10
    color = Config.red

    def __init__(self, pos):
        super().__init__(pos)
