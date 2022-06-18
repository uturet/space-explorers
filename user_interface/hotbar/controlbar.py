from user_interface import Node, Button
import pygame
from core.config import Config
from game_objects.buildings import Generator


class ControlBar(Node):
    info_provider = None

    def __init__(self, parent, width, height, shift):
        self.width = width
        self.height = height
        super().__init__(parent)
        self.rect.left = shift

        # self.destroy_button = Button(
        #     self, parent.mod_index, color=Config.red_500,
        #     on_mouseup=self.handle_destroy_provider)
        # self.destroy_button.rect.topleft = (200, 0)
        # self.mods = [
        #     GeneratorControlBar(self, parent.mod_index)
        # ]

        # self.cur_mod = None

    def draw_controlbar(self):
        self.image.blit(
            self.destroy_button.image, self.destroy_button.rect.topleft)
        if self.cur_mod:
            for btn in self.cur_mod.buttons:
                self.image.blit(btn.image, btn.rect.topleft)

    def set_info_provider(self, sprite):
        self.cur_mod = None
        self.info_provider = sprite
        for mod in self.mods:
            if isinstance(sprite, mod.controls):
                self.cur_mod = mod
                mod.set_building(sprite)
        self.draw_controlbar()

    def handle_destroy_provider(self, state, event):
        print('destroy')
        # pygame.event.post(pygame.event.Event(HOTBARSELECTMOD))


class DestroyButton(Button):
    color = Config.red_500

    def __init__(self, parent, mod_index, handler):
        super().__init__(parent, mod_index)
        self.handler = handler

    def handle_mousebuttonup(self, state, event):
        if (state.hotbar.active_mod_index == self.mod_index and
                self in state.mouse_intersected):
            self.handler()


class GeneratorControlBar:
    controls = Generator

    def __init__(self, parent, mod_index):
        self.buttons = []
        self.building = None
        self.create_controlbar(parent, mod_index)

    def set_building(self, building):
        self.building = building

    def create_controlbar(self, parent, mod_index):
        font = pygame.font.SysFont(pygame.font.get_default_font(), 30)
        b = Button(parent, mod_index, on_mouseup=self.set_p_build,
                   color=Config.green_500)
        b.rect.left = b.rect.width * len(self.buttons)
        image = font.render('Bu', False, (255, 255, 255))
        b.image.blit(image, (2, 2))
        self.buttons.append(b)

        b = Button(parent, mod_index, on_mouseup=self.set_p_charge,
                   color=Config.blue_500)
        b.rect.left = b.rect.width * len(self.buttons)
        self.buttons.append(b)
        image = font.render('Ch', False, (255, 255, 255))
        b.image.blit(image, (2, 2))

        b = Button(parent, mod_index, on_mouseup=self.set_p_heal,
                   color=Config.amber_500)
        b.rect.left = b.rect.width * len(self.buttons)
        self.buttons.append(b)
        image = font.render('He', False, (255, 255, 255))
        b.image.blit(image, (2, 2))

        b = Button(parent, mod_index, on_mouseup=self.set_es_broadcast,
                   color=Config.pink_200)
        b.rect.left = b.rect.width * len(self.buttons) + 30
        self.buttons.append(b)
        image = font.render('Br', False, (255, 255, 255))
        b.image.blit(image, (2, 2))

        b = Button(parent, mod_index, on_mouseup=self.set_es_direct,
                   color=Config.amber_500)
        b.rect.left = (b.rect.width * len(self.buttons)) + 30
        self.buttons.append(b)
        image = font.render('Di', False, (255, 255, 255))
        b.image.blit(image, (2, 2))

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
