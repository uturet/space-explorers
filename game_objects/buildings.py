import pygame
from game_objects.object_type import Building, Preview
from core.config import Config
from core.event import HOTBARINFOMOD
from core.animation import Frame


class Transmitter(Building):
    size = 20
    radius = 10
    color = Config.blue_500
    hover_color = Config.blue_200
    active_color = Config.green_200

    def __init__(self, building_con, pos):
        super().__init__(building_con, pos)
        self.paint()

    def paint(self):
        pygame.draw.circle(self._image, self.color,
                           (self.radius, self.radius), self.radius)
        if self.is_hover:
            pygame.draw.circle(self._image, self.hover_color,
                               (self.radius, self.radius), self.radius, 2
                               )
        if self.is_active:
            pygame.draw.circle(self._image, self.active_color,
                               (self.radius, self.radius), self.radius, 2
                               )
        self.image = self._image.convert_alpha()

    def update(self, state):
        pass

    def draw(self, state):
        for con in self.building_con.values():
            con.draw(state)
        self.paint()

    def handle_mousebuttonup(self, state, event):
        if (self in state.mouse_intersected
                and not self.is_active):
            self.paint()
            pygame.event.post(pygame.event.Event(
                HOTBARINFOMOD, {'sprite': self}))

    def activate(self):
        self.is_active = True
        for con in self.building_con.values():
            con.activate()

    def deactivate(self):
        if self.is_active:
            self.is_active = False
            self.paint()
            for con in self.building_con.values():
                con.deactivate()


class TransmitterPreview(Preview):
    building = Transmitter

    width = 20
    height = 20
    option_radius = 40
    radius = Transmitter.radius
    small_option_radius = 20

    color = Config.blue_500
    preview_color = Config.blue_200

    def create_preview_frames(self):
        for color in (self.preview_color, self.invalid_preview_color):
            image = pygame.Surface(
                (self.width, self.height), pygame.SRCALPHA)
            pygame.draw.circle(image, color,
                               self.rect.center, self.radius)
            converted = image.convert_alpha()
            self.frames.append(
                Frame(converted, pygame.mask.from_surface(converted)))

    def draw_option_image(self, rect, image=None):
        if image:
            pygame.draw.circle(image, self.color,
                               rect.center, self.option_radius)
        else:
            pygame.draw.circle(self.option_image, self.color,
                               rect.center, self.option_radius)

    def draw_small_option_image(self, rect, image=None):
        if image:
            pygame.draw.circle(image, self.color, rect.center,
                               self.small_option_radius)
        else:
            pygame.draw.circle(self.option_image, self.color, rect.center,
                               self.small_option_radius)


building_previews = {}
