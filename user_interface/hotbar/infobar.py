from game_objects.object_type import Building
from user_interface import Node
from game_objects.buildings import building_previews
from core.config import Config
from game_objects.buildings import Generator, LaserGun
import pygame
from core import collision_handler as ch
from collections import namedtuple
import math
import random


class InfoBar(Node):
    width = Config.hotbarwidth
    height = Config.hotbarheight

    def __init__(self):
        super().__init__()
        self.info_provider = None
        self.btngroups = [
            GeneratorControlBar(),
            LaserGunControlBar(),
        ]
        self.cur_btngroup = None

    def set_info_provider(self, sprite):
        self.info_provider = sprite
        for btngroup in self.btngroups:
            if isinstance(sprite, btngroup.controls):
                btngroup.set_building(sprite)
                self.cur_btngroup = btngroup
                break
        sprite.set_ui_type(Building.SELECTED)

    def handle_mousebuttonup(self, state, event):
        if self.cur_btngroup:
            self.cur_btngroup.handle_mousebuttonup(state, event)

    def draw(self):
        self.image.fill((255, 255, 255, 0))
        if self.cur_btngroup:
            (building_previews[self.cur_btngroup.building.__class__.__name__]
             .draw_option_image(
                (self.height/2, self.height/2), self.image))
        if self.cur_btngroup:
            self.cur_btngroup.draw(self.image)


class MultiInfoBar(Node):
    width = Config.hotbarwidth
    height = Config.hotbarheight
    group_height = 40

    def __init__(self):
        super().__init__()
        self.btngroups = [
            GeneratorControlBar(),
            LaserGunControlBar(),
        ]
        self.groups = [[] for i in range(len(self.btngroups))]
        self.groups_images = []
        self.cur_btngroup = 0
        self.groups_image = pygame.Surface(
            (self.height+15, self.group_height*len(building_previews)), pygame.SRCALPHA)
        self.groups_rect = self.groups_image.get_rect()
        self.create_groups_images()

    def set_info_providers(self, sprites):
        self.cur_btngroup = 0
        self.groups = [[] for i in range(len(self.btngroups))]
        for spr in sprites:
            for index, btngroup in enumerate(self.btngroups):
                if isinstance(spr, btngroup.controls):
                    self.groups[index].append(spr)
                    break

    def create_groups_images(self):
        size = 14
        cross = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.line(cross, (255, 255, 255), (0, 0), (size, size), 4)
        pygame.draw.line(cross, (255, 255, 255), (-1, size), (size, -1), 4)

        for index, preview in enumerate(building_previews.values()):
            self.groups_images.append([])
            for active in (False, True):
                image = pygame.Surface(
                    (self.groups_rect.width, 40), pygame.SRCALPHA)
                rect = image.get_rect()
                preview.draw_small_option_image(
                    (rect.height/2, rect.height/2), image)
                if active:
                    pygame.draw.rect(image, (255, 255, 255),
                                     (0, 0, rect.width, rect.height), 2)
                image.blit(cross, (45, 13))
                self.groups_images[index].append(Frame(image, rect))

    def handle_mousebuttonup(self, state, event):
        if event.button == 1:
            if event.pos[0] <= self.groups_rect.width:
                index = int(
                    (event.pos[1]-self.groups_rect.top)/self.group_height)
                if 0 <= index <= len(self.groups_images):
                    self.cur_btngroup = index
            else:
                event.pos = (event.pos[0]-self.groups_rect.width, event.pos[1])

    def handle_mousewheel(self, state, event):
        self.groups_rect.center = (
            self.groups_rect.centerx,
            self.groups_rect.centery +
            ((event.x+event.y) * self.group_height))

    def draw(self):
        self.image.fill((255, 255, 255, 0))
        self.groups_image.fill((255, 255, 255, 0))
        font = pygame.font.SysFont(pygame.font.get_default_font(), 35)
        for index, group in enumerate(self.groups_images):
            text = font.render(
                f'{random.randint(0, 1000)}', False, (255, 255, 255))
            if index == self.cur_btngroup:
                self.groups_image.blit(group[1].image, (0, index*40))
            else:
                self.groups_image.blit(group[0].image, (0, index*40))
            self.groups_image.blit(text, (70, (index*40)+9))
        self.image.blit(self.groups_image, self.groups_rect.topleft)


Button = namedtuple('Button', 'default active handler')
Frame = namedtuple('Frame', 'image rect')


class ToggleGroupsManager:
    def __init__(self):
        self.groups = []
        self.selected = []

    def handle_mousebuttonup(self, state, event):
        for index, group in enumerate(self.groups):
            for i, button in enumerate(group):
                if ch.is_pos_intersects_rect(event.pos, button.default.rect):
                    button.handler(state, event)
                    self.selected[index] = i
                    return

    def draw(self, image):
        for index, group in zip(self.selected, self.groups):
            for i, button in enumerate(group):
                if index == i:
                    image.blit(button.active.image, button.active.rect)
                else:
                    image.blit(button.default.image, button.default.rect)

    def create_group(self, start_pos, titles, handlers):
        font = pygame.font.SysFont(pygame.font.get_default_font(), 20)
        group = []
        for i, text in enumerate(titles):
            pos = (start_pos[0] + ((i*(40+10))), start_pos[1])
            df = self.create_frame(font, text, pos)
            af = self.create_frame(font, text, pos, True)
            group.append(
                Button(default=df, active=af, handler=handlers[i]))
        self.groups.append(group)
        self.selected.append(0)

    def create_frame(self, font, text, topleft=(0, 0), active=False):
        dimens = (40, 30)
        image = pygame.Surface(dimens)
        image.fill(Config.amber_500)
        rect = image.get_rect()
        rect.topleft = topleft
        text = font.render(text, False, (0, 0, 0))
        if active:
            pygame.draw.rect(image, (0, 0, 0),
                             (0, 0, *dimens), 3)
        image.blit(text, (4, 7))
        image = image.convert_alpha()
        return Frame(image, rect)


class GeneratorControlBar(ToggleGroupsManager):
    controls = Generator

    def __init__(self):
        super().__init__()
        self.building = None
        self.pgroup = ('BUILD', 'CHARGE', 'HEAL')
        self.handler_pgroup = (
            self.set_p_build, self.set_p_charge, self.set_p_heal)
        self.esgroup = ('BROADCAST', 'DIRECT')
        self.handler_esgroup = (
            self.set_es_broadcast, self.set_es_direct)
        self.create_controlbar()

    def set_building(self, building):
        self.building = building
        self.selected[0] = building._p_type
        self.selected[1] = building._es_type

    def create_controlbar(self):
        self.create_group((100, 40), self.pgroup, self.handler_pgroup)
        self.create_group((260, 40), self.esgroup, self.handler_esgroup)

    def set_p_build(self, state, event):
        self.building._p_type = Generator.BUILD

    def set_p_charge(self, state, event):
        self.building._p_type = Generator.CHARGE

    def set_p_heal(self, state, event):
        self.building._p_type = Generator.HEAL

    def set_es_broadcast(self, state, event):
        self.building._es_type = Generator.BROADCAST

    def set_es_direct(self, state, event):
        self.building._es_type = Generator.DIRECT


class LaserGunControlBar(ToggleGroupsManager):
    controls = LaserGun

    def __init__(self):
        super().__init__()
        self.building = None
        self.fgroup = ('HOLD', 'FIRE')
        self.handler_fgroup = (self.set_fire, self.set_fire)
        self.create_controlbar()

    def set_building(self, building):
        self.building = building
        self.selected[0] = int(building.fire)

    def create_controlbar(self):
        self.create_group((100, 40), self.fgroup, self.handler_fgroup)

    def set_fire(self, state, event):
        self.building.fire = not self.building.fire
