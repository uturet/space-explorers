import pygame
from game_objects.object_type import Building, Preview
from core.config import Config
from core.property import (
    EnergySpreader, Battery, EnergyInteraction, Gun)
from core.animation import Frame
import math

from game_objects.particles import LightBeem

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

    def draw_option_image(self, center, image):
        pygame.draw.circle(image, self.color,
                           center, self.option_radius)

    def draw_small_option_image(self, center, image):
        pygame.draw.circle(image, self.color, center,
                           self.small_option_radius)


class Generator(Building, Battery, EnergySpreader):

    width = 40
    height = width
    radius = width/2
    color = Config.green_500

    health = 200
    capacity = 100
    charge = 0
    chargable = False
    production = 0

    _default_ei_type = EnergyInteraction.PRODUCER

    BUILD = 0
    CHARGE = 1
    HEAL = 2
    _p_type = BUILD

    def activate(self, state):
        super().activate(state)
        self.production = 10

    def draw_frame(self, image, color):
        pygame.draw.circle(image, color,
                           (self.radius, self.radius), self.radius)

    def update(self, state):
        e = round(state.seconds * self.production, 4)
        self.charge = min(self.capacity, self.charge + e)

        if (self in state.path_manager.paths and
                len(state.path_manager.paths[self])):
            cur_consumer = None
            cur_path = None
            for consumer, path in state.path_manager.paths[self].items():

                if consumer.chargable:
                    if (consumer.undamaged and
                            consumer.full):
                        continue
                else:
                    if consumer.undamaged:
                        continue

                if cur_consumer is None:
                    cur_consumer = consumer
                    cur_path = path
                elif self._p_type == Generator.BUILD:
                    if cur_consumer._type == Building.PLAN:
                        continue
                    elif consumer._type == Building.PLAN:
                        cur_consumer = consumer
                        cur_path = path
                elif self._p_type == Generator.CHARGE:
                    if cur_consumer.chargable and not cur_consumer.full:
                        continue
                    elif consumer.chargable and not consumer.full:
                        cur_consumer = consumer
                        cur_path = path
                elif self._p_type == Generator.HEAL:
                    if (not cur_consumer.undamaged or
                        consumer._type == Building.PLAN or
                            consumer.undamaged):
                        continue
                    elif consumer.undamaged:
                        cur_consumer = consumer
                        cur_path = path

            if cur_consumer is None:
                return
            e = round(state.seconds * THROUGHPUT, 4)
            if self.charge > e:
                self.charge -= e
            else:
                e = self.charge
                self.charge = 0
            cur_consumer.receie_energy(state, e)
            for con in cur_path:
                con.activate()

            if (self._es_type == EnergySpreader.DIRECT or self.charge == 0):
                pass


class GeneratorPreview(Preview):
    building = Generator
    preview_color = Config.green_200

    def draw_frame(self, image, color):
        pygame.draw.circle(image, color,
                           self.rect.center, self.radius)

    def draw_option_image(self, center, image):
        pygame.draw.circle(image, self.color,
                           center, self.option_radius)

    def draw_small_option_image(self, center, image):
        pygame.draw.circle(image, self.color, center,
                           self.small_option_radius)


class LaserGun(Building, Battery, Gun):

    width = 40
    height = width
    radius = width/2
    color = Config.purple_500

    health = 50
    capacity = 150
    charge = 0
    chargable = True

    power = 50

    fire = True

    _default_ei_type = EnergyInteraction.CONSUMER

    def __init__(self, pos):
        super().__init__(pos)
        self.light_beem = LightBeem((
            self.rect.right+2, self.rect.centery
        ))

    def receie_energy(self, state, charge):
        if self.health_point == self.health:
            self.charge += charge
            if self.charge >= self.capacity:
                self.charge = self.capacity
        else:
            self.health_point += charge
            if self.health_point >= self.health:
                self.health_point = self.health
                if self._type == Building.PLAN:
                    self.activate(state)

    def activate(self, state):
        self._type = Building.ACTIVE
        self._ei_type = self._default_ei_type
        self.select_frame()

    def draw_frame(self, image, color):
        pygame.draw.circle(image, color,
                           (self.radius, self.radius), self.radius)

    def update(self, state):
        if self._type == Building.PLAN:
            return
        if self.charge == self.capacity:
            self.fire = True
        if self.charge:
            e = state.seconds * self.power
            if e < self.charge and self.fire:
                self.charge -= e
                self.light_beem.fire = True
            else:
                self.fire = False
                self.light_beem.fire = False
        else:
            self.light_beem.fire = False


class LaserGunPreview(Preview):
    building = LaserGun
    preview_color = Config.purple_200

    def draw_frame(self, image, color):
        pygame.draw.circle(image, color,
                           self.rect.center, self.radius)

    def draw_option_image(self, center, image):
        pygame.draw.circle(image, self.color,
                           center, self.option_radius)

    def draw_small_option_image(self, center, image):
        pygame.draw.circle(image, self.color, center,
                           self.small_option_radius)


building_previews = {}
