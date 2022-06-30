import pygame
from game_objects.object_type import Building, Preview
from core.config import Config
from core.property import (
    EnergySpreader, Battery, EnergyInteraction, Gun)
from core import helpers as ch
import math

from game_objects.particles import LightBeem

THROUGHPUT = 100


class Transmitter(Building):
    health = 100

    width = 20
    height = width
    radius = width/2
    color = Config.blue_500

    def draw_frame(self, image, color, index=None):
        pygame.draw.circle(image, color,
                           (self.radius, self.radius), self.radius)


class TransmitterPreview(Preview):
    building = Transmitter
    preview_color = Config.blue_200

    def draw_frame(self, image, color, index=None):
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

    def set_priority(self, p):
        self._p_type = p

    _es_type = EnergySpreader.BROADCAST

    def activate(self, state):
        super().activate(state)
        self.production = 10

    def draw_frame(self, image, color, index=None):
        pygame.draw.circle(image, color,
                           (self.radius, self.radius), self.radius)

    def update(self, state):
        e = round(state.seconds * self.production, 4)
        self.charge = min(self.capacity, self.charge + e)

        if (self._type != Building.DESTROY and self in state.path_manager.paths and
                len(state.path_manager.paths[self])):
            priority = [([], []), ([], []), ([], [])]
            for consumer, path in state.path_manager.paths[self].items():
                if (consumer._type == Building.PLAN or
                        consumer._type == Building.DESTROY):
                    priority[self.BUILD][0].append(consumer)
                    priority[self.BUILD][1].append(path)
                if consumer.chargable:
                    if (consumer.undamaged and
                            consumer.full):
                        continue
                else:
                    if consumer.undamaged:
                        continue
                if consumer.chargable and not consumer.full:
                    priority[self.CHARGE][0].append(consumer)
                    priority[self.CHARGE][1].append(path)
                if not consumer.undamaged:
                    priority[self.HEAL][0].append(consumer)
                    priority[self.HEAL][1].append(path)

            next_p_type = self._p_type
            if not len(priority[self._p_type][0]):
                if len(priority[self.BUILD][0]):
                    next_p_type = self.BUILD
                elif len(priority[self.CHARGE][0]):
                    next_p_type = self.CHARGE
                elif len(priority[self.HEAL][0]):
                    next_p_type = self.HEAL

            if self._es_type == EnergySpreader.BROADCAST:
                e = round(state.seconds * THROUGHPUT, 4)
                if e * len(priority[next_p_type][0]) > self.charge:
                    e = round(self.charge / len(priority[next_p_type][0]), 4)
                    self.charge = 0
                else:
                    self.charge -= e * len(priority[next_p_type][0])
                for consumer, path in zip(
                        priority[next_p_type][0], priority[next_p_type][1]):
                    consumer.receie_energy(state, e)
                    for con in path:
                        con.activate()
            elif (self._es_type == EnergySpreader.DIRECT and
                  len(priority[next_p_type][0])):
                e = round(state.seconds * THROUGHPUT, 4)
                if self.charge > e:
                    self.charge -= e
                else:
                    e = self.charge
                    self.charge = 0
                priority[next_p_type][0][0].receie_energy(state, e)
                for con in priority[next_p_type][1][0]:
                    con.activate()


class GeneratorPreview(Preview):
    building = Generator
    preview_color = Config.green_200

    def draw_frame(self, image, color, index=None):
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

    power = 10

    _default_ei_type = EnergyInteraction.CONSUMER

    def __init__(self, pos, angle):
        self.angle = angle
        super().__init__(pos)
        self.light_beem = LightBeem(self.rect.center, angle)

    def activate(self, state):
        self._type = Building.ACTIVE
        self._ei_type = self._default_ei_type
        self.select_frame()

    def draw_frame(self, image, color, index=None):
        pygame.draw.circle(image, color,
                           (self.radius, self.radius), self.radius)
        end_pos = ch.get_line(
            (self.radius, self.radius),
            (self.width, self.radius),
            self.angle, 19)
        pygame.draw.line(image, Config.amber_500,
                         (self.radius, self.radius), end_pos, width=2)

    def update(self, state):
        if self._type == Building.PLAN:
            return
        if self.charge == self.capacity:
            self.light_beem.fire = True
        if self.fire and self.charge:
            e = state.seconds * self.power
            if e < self.charge:
                self.charge -= e
                self.light_beem.fire = True
            else:
                self.light_beem.fire = False
        else:
            self.light_beem.fire = False

    def close(self, state):
        self.light_beem.fire = False
        state.partgroup.remove(self.light_beem)

    def cover_area(self, pos):
        self.gun_pimage.fill((255, 255, 255, 0))
        self.gun_rect.center = (800, 600)
        pm1, pm2 = self.get_line(self.gun_rect.center, pos, angle=0)
        p1, p2 = self.get_line(self.gun_rect.center, pos)
        p3, p4 = self.get_line(self.gun_rect.center, pos, opposit=True)
        r2 = self.get_rad(p1, self.gun_rect.center)
        r1 = self.get_rad(p3, self.gun_rect.center)

        pcm1, pcm2 = self.get_line(self.gun_rect.center,
                                   self.mouse.pos, angle=0)

        rcm = self.get_rad(pcm2, pcm1)
        rm = self.get_rad(pm2, pm1)
        pc1, pc2 = self.get_line(self.gun_rect.center,
                                 pm1, angle=0.02)
        pc3, pc4 = self.get_line(self.gun_rect.center,
                                 pm1, angle=-0.02)
        if r1 > r2:
            if r1 <= rcm <= 2*math.pi or 0 <= rcm <= r2:
                pc1, pc2 = self.get_line(self.gun_rect.center,
                                         self.mouse.pos, angle=0.02)
                pc3, pc4 = self.get_line(self.gun_rect.center,
                                         self.mouse.pos, angle=-0.02)

        else:
            if r1 <= rcm <= r2:
                pc1, pc2 = self.get_line(self.gun_rect.center,
                                         self.mouse.pos, angle=0.02)
                pc3, pc4 = self.get_line(self.gun_rect.center,
                                         self.mouse.pos, angle=-0.02)
        rc2 = self.get_rad(pc2, pc1)
        rc1 = self.get_rad(pc4, pc3)
        pygame.draw.arc(
            self.gun_pimage,
            Config.red_500,
            (0, 0, 400, 400), rm-math.pi/6, rm+math.pi/6, 100)
        self.gun_pimage.set_alpha(50)

        pygame.draw.arc(
            self.screen,
            Config.amber_500,
            self.gun_rect, rc1, rc2, 100)

    @staticmethod
    def get_rad(pos1, pos2, positive=True):
        r = math.atan2(pos2[1]-pos1[1],
                       pos1[0]-pos2[0])
        if r < 0 and positive:
            r += math.pi*2
        return r

    def laser_gun_precreate(self):
        circle = pygame.Surface((400, 400), pygame.SRCALPHA)
        circle.set_alpha(70)
        pygame.draw.circle(circle, Config.red_500, (200, 200), 200)
        image = pygame.Surface((400, 400), pygame.SRCALPHA)
        image.blit(circle, (0, 0))

        self.gun_pimage = image
        self.gun_rect = image.get_rect()


class LaserGunPreview(Preview):
    building = LaserGun
    preview_color = Config.purple_200
    angle = 0

    def draw_frame(self, image, color, index=None):
        pygame.draw.circle(image, color,
                           self.rect.center, self.radius)

    def draw_option_image(self, center, image):
        pygame.draw.circle(image, self.color,
                           center, self.option_radius)

    def draw_small_option_image(self, center, image):
        pygame.draw.circle(image, self.color, center,
                           self.small_option_radius)

    def handle_mousewheel(self, state, event):
        self.angle += 0.085 * event.y
        self.draw_image(state)

    def draw_image(self, state):
        state.mouse.image.blit(self.image, self.center_point)
        start_pos = (self.center_point[0]+self.building.radius,
                     self.center_point[1]+self.building.radius)
        end_pos = ch.get_line(
            start_pos,
            (self.center_point[0]+self.building.width,
             self.center_point[1]+self.building.radius),
            self.angle, 19)
        pygame.draw.line(state.mouse.image, Config.amber_500,
                         start_pos, end_pos, width=2)

    def create_building(self, pos):
        return self.building(pos, self.angle)


building_previews = {}
