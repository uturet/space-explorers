import pygame
from game_objects.object_type import Building, Preview
from core.config import Config
from core.property import EnergySpreader, Battery, EnergyInteraction

THROUGHPUT = 100


class Transmitter(Building):
    health = 100

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


class Generator(Building, Battery, EnergySpreader):

    width = 40
    height = width
    radius = width/2
    color = Config.green_500

    health = 200
    capacity = 100
    charge = 0
    production = 10

    _default_ei_type = EnergyInteraction.PRODUCER

    def draw_frame(self, image, color):
        pygame.draw.circle(image, color,
                           (self.radius, self.radius), self.radius)

    def update(self, state):
        e = round(state.seconds * self.production, 4)
        self.charge = min(self.capacity, self.charge + e)

        if (self in state.path_manager.paths and
                len(state.path_manager.paths[self])):
            for consumer, path in state.path_manager.paths[self].items():
                e = round(state.seconds * THROUGHPUT, 4)
                if self.charge > e:
                    self.charge -= e
                else:
                    e = self.charge
                    self.charge = 0
                consumer.receie_energy(state, e)
                for con in path:
                    con.activate()

                if (self._es_type == EnergySpreader.DIRECT or self.charge == 0):
                    break


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
