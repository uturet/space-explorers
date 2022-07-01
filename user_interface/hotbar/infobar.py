from game_objects.buildings import Transmitter, building_previews
from game_objects.buildings import Generator, LaserGun
from game_objects.object_type import Building
from core.property import EnergyInteraction
from collections import namedtuple
from user_interface import Node
from core.config import Config
from core import helpers as ch
import pygame


class ControlBar(Node):

    def __init__(self):
        super().__init__()
        self.info_provider = None
        self.req_btngroups = {
            BuildingBtnGroup.controls.__name__: BuildingBtnGroup(),
        }
        self.btngroups = {
            TransmitterBtnGroup.controls.__name__: TransmitterBtnGroup(),
            GeneratorBtnGroup.controls.__name__: GeneratorBtnGroup(),
            LaserGunBtnGroup.controls.__name__: LaserGunBtnGroup(),
        }
        self.cur_gtype = None


class InfoBar(ControlBar):
    width = Config.hotbarwidth
    height = Config.hotbarheight

    def set_info_provider(self, sprite):
        self.info_provider = sprite
        for gtype, btngroup in self.btngroups.items():
            if isinstance(sprite, btngroup.controls):
                btngroup.set_building(sprite)
                self.cur_gtype = gtype
                break
        for btngroup in self.req_btngroups.values():
            if isinstance(sprite, btngroup.controls):
                btngroup.set_building(sprite)
        sprite.set_ui_type(Building.SELECTED)

    def handle_mousebuttonup(self, state, event):
        if self.cur_gtype in self.btngroups:
            self.btngroups[self.cur_gtype].handle_mousebuttonup(state, event)
        for btngorup in self.req_btngroups.values():
            if isinstance(self.info_provider, btngorup.controls):
                btngorup.handle_mousebuttonup(state, event)

    def draw(self):
        self.image.fill((255, 255, 255, 0))
        if self.cur_gtype in self.btngroups:
            (building_previews[
                self.btngroups[self.cur_gtype]
                .controls.__name__]
             .draw_option_image(
                (self.height/2, self.height/2), self.image))
            self.btngroups[self.cur_gtype].draw(self.image)
        for btngorup in self.req_btngroups.values():
            if isinstance(self.info_provider, btngorup.controls):
                btngorup.draw(self.image)


class MultiInfoBar(ControlBar):
    width = Config.hotbarwidth
    height = Config.hotbarheight
    group_height = 40

    def __init__(self):
        super().__init__()
        self.groups = {}
        self.groups_images = {}
        self.groups_image = pygame.Surface(
            (self.height, self.group_height*len(building_previews)), pygame.SRCALPHA)
        self.groups_rect = self.groups_image.get_rect()
        self.create_groups_images()

    def set_info_providers(self, sprites):
        self.cur_gtype = None
        self.groups = {}
        for spr in sprites:
            if self.cur_gtype is None:
                self.cur_gtype = spr.__class__.__name__
            if spr.__class__.__name__ not in self.groups:
                self.groups[spr.__class__.__name__] = []
            self.groups[spr.__class__.__name__].append(spr)
        for gtype, group in self.groups.items():
            if gtype in self.btngroups:
                self.btngroups[gtype].set_buildings(group)

    def create_groups_images(self):
        size = 10
        cross = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.line(cross, (255, 255, 255), (0, 0), (size, size), 3)
        pygame.draw.line(cross, (255, 255, 255), (-1, size), (size, -1), 3)

        for spr_type, preview in building_previews.items():
            self.groups_images[spr_type] = []
            for active in (False, True):
                image = pygame.Surface(
                    (self.groups_rect.width, 40), pygame.SRCALPHA)
                rect = image.get_rect()
                preview.draw_small_option_image(
                    (rect.height/2, rect.height/2), image)
                if active:
                    pygame.draw.rect(image, (255, 255, 255),
                                     (0, 0, rect.width, rect.height), 2)
                image.blit(cross, (40, 15))
                self.groups_images[spr_type].append(Frame(image, rect))

    def handle_mousebuttonup(self, state, event):
        if event.button == 1:
            if event.pos[0] <= self.groups_rect.width:
                index = int(
                    (event.pos[1]-self.groups_rect.top)/self.group_height)
                if 0 <= index <= len(self.groups):
                    self.cur_gtype = list(self.groups.keys())[index]
            elif (self.cur_gtype in self.btngroups):
                self.btngroups[self.cur_gtype].handle_mousebuttonup(
                    state, event)

    def handle_mousewheel(self, state, event):
        self.groups_rect.center = (
            self.groups_rect.centerx,
            self.groups_rect.centery +
            ((event.x+event.y) * self.group_height))

    def draw(self):
        self.image.fill((255, 255, 255, 0))
        self.groups_image.fill((255, 255, 255, 0))
        font = pygame.font.SysFont(pygame.font.get_default_font(), 35)

        index = 0
        for gtype, group in self.groups.items():
            if self.cur_gtype is None:
                self.cur_gtype = gtype
            text = font.render(
                f'{len(group)}', False, (255, 255, 255))
            if self.cur_gtype == gtype:
                self.groups_image.blit(
                    self.groups_images[gtype][1].image, (0, index*40))
            else:
                self.groups_image.blit(
                    self.groups_images[gtype][0].image, (0, index*40))
            self.groups_image.blit(text, (70, (index*40)+9))
            index += 1
        if self.cur_gtype in self.btngroups:
            self.btngroups[self.cur_gtype].draw(self.image)
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

    def create_group(self, start_pos, titles, handlers, color=Config.amber_500):
        font = pygame.font.SysFont(pygame.font.get_default_font(), 20)
        group = []
        for i, text in enumerate(titles):
            pos = (start_pos[0] + ((i*(40+10))), start_pos[1])
            df = self.create_frame(font, text, color, pos)
            af = self.create_frame(font, text, color, pos, True)
            group.append(
                Button(default=df, active=af, handler=handlers[i]))
        self.groups.append(group)
        self.selected.append(None)

    def create_frame(self, font, text, color, topleft=(0, 0), active=False):
        dimens = (40, 30)
        image = pygame.Surface(dimens)
        image.fill(color)
        rect = image.get_rect()
        rect.topleft = topleft
        text = font.render(text, False, (0, 0, 0))
        if active:
            pygame.draw.rect(image, (0, 0, 0),
                             (0, 0, *dimens), 3)
        image.blit(text, (4, 7))
        image = image.convert_alpha()
        return Frame(image, rect)


class BuildingBtnGroup(ToggleGroupsManager):
    controls = Building
    building = None

    def __init__(self):
        super().__init__()
        self.dgroup = ('DESTROY', )
        self.handler_dgroup = (self.destroy, )
        self.create_controlbar()

    def set_building(self, building):
        self.building = building
        self.selected[0] = int(building._type != Building.DESTROY)

    def create_controlbar(self):
        self.create_group(
            (460, 0), self.dgroup,
            self.handler_dgroup, Config.red_500)

    def destroy(self, state, event):
        if self.building.type != Building.DESTROY:
            self.building.type = Building.DESTROY
            self.building.ei_type = EnergyInteraction.CONSUMER
            # state.path_manager.remove_producer(self.building)


class TransmitterBtnGroup(ToggleGroupsManager):
    controls = Transmitter

    def set_building(self, building):
        pass

    def set_buildings(self, building):
        pass


class GeneratorBtnGroup(ToggleGroupsManager):
    controls = Generator
    building = None
    buildings = None

    def __init__(self):
        super().__init__()
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

    def set_buildings(self, buildings):
        self.buildings = buildings
        self.selected[0] = buildings[0]._p_type
        self.selected[1] = buildings[0]._es_type
        for b in buildings:
            if b._p_type != self.selected[0]:
                self.selected[0] = None
            if b._es_type != self.selected[1]:
                self.selected[1] = None

    def create_controlbar(self):
        self.create_group((100, 40), self.pgroup, self.handler_pgroup)
        self.create_group((260, 40), self.esgroup, self.handler_esgroup)

    def set_p_build(self, state, event):
        if self.building:
            self.building._p_type = Generator.BUILD
        elif self.buildings:
            for b in self.buildings:
                b._p_type = Generator.BUILD

    def set_p_charge(self, state, event):
        if self.building:
            self.building._p_type = Generator.CHARGE
        elif self.buildings:
            for b in self.buildings:
                b._p_type = Generator.CHARGE

    def set_p_heal(self, state, event):
        if self.building:
            self.building._p_type = Generator.HEAL
        elif self.buildings:
            for b in self.buildings:
                b._p_type = Generator.HEAL

    def set_es_broadcast(self, state, event):
        if self.building:
            self.building._es_type = Generator.BROADCAST
        elif self.buildings:
            for b in self.buildings:
                b._es_type = Generator.BROADCAST

    def set_es_direct(self, state, event):
        if self.building:
            self.building._es_type = Generator.DIRECT
        elif self.buildings:
            for b in self.buildings:
                b._es_type = Generator.DIRECT


class LaserGunBtnGroup(ToggleGroupsManager):
    controls = LaserGun
    building = None

    def __init__(self):
        super().__init__()
        self.fgroup = ('HOLD', 'FIRE')
        self.handler_fgroup = (self.set_hold, self.set_fire)
        self.create_controlbar()

    def set_building(self, building):
        self.building = building
        self.selected[0] = int(building.fire)

    def set_buildings(self, buildings):
        self.buildings = buildings
        self.selected[0] = int(buildings[0].fire)
        for b in buildings:
            if b.fire != self.selected[0]:
                self.selected[0] = None

    def create_controlbar(self):
        self.create_group((100, 40), self.fgroup, self.handler_fgroup)

    def set_fire(self, state, event):
        if self.building:
            self.building.fire = 1
        elif self.buildings:
            if self.selected[0] is None:
                self.selected[0] = 1
            for b in self.buildings:
                b.fire = 1

    def set_hold(self, state, event):
        if self.building:
            self.building.fire = 0
        elif self.buildings:
            if self.selected[0] is None:
                self.selected[0] = 0
            for b in self.buildings:
                b.fire = 0
