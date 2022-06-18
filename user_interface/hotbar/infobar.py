from game_objects.object_type import Building
from user_interface import Node
from game_objects.buildings import building_previews
from core.config import Config
from game_objects.buildings import Generator
import pygame
from core import collision_handler as ch
from collections import namedtuple


class InfoBar(Node):
    width = Config.hotbarwidth
    height = Config.hotbarheight

    def __init__(self):
        super().__init__()
        self.info_provider = None
        self.btngroups = [
            GeneratorControlBar(),
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
        building_previews[sprite.__class__.__name__].draw_option_image(
            (self.height/2, self.height/2), self.image)

    def handle_mousebuttonup(self, state, event):
        if self.cur_btngroup:
            event.pos = (event.pos[0] - self.rect.left,
                         event.pos[1] - self.rect.top)
            self.cur_btngroup.handle_mousebuttonup(state, event)

    def draw(self):
        if self.cur_btngroup:
            self.cur_btngroup.draw(self.image)


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

    def set_p_build(self, state, event):
        if self.building:
            self.building._p_type = Generator.BUILD

    def set_p_charge(self, state, event):
        if self.building:
            self.building._p_type = Generator.CHARGE

    def set_p_heal(self, state, event):
        if self.building:
            self.building._p_type = Generator.HEAL

    def set_es_broadcast(self, state, event):
        if self.building:
            self.building._es_type = Generator.BROADCAST

    def set_es_direct(self, state, event):
        if self.building:
            self.building._es_type = Generator.DIRECT
