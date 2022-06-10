import pygame
from game_objects.object_types import Building, Preview
from core.config import Config
from core.event import HOTBARINFOMOD


class Transmitter(Building):
    size = 20
    radius = 10
    color = Config.blue_500
    hover_color = Config.blue_200
    active_color = Config.green_200

    def __init__(self, pos):
        super().__init__(pos)
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
        self.paint()

    def handle_mousebuttonup(self, state, event):
        if self in state.mouse_intersected:
            self.is_active = True
            self.paint()
            pygame.event.post(pygame.event.Event(
                HOTBARINFOMOD, {'sprite': self}))
        elif self.is_active:
            self.is_active = False
            self.paint()


class TransmitterPreview(Preview):
    building = Transmitter

    width = 20
    height = 20

    cover_size = 200
    cover_radius = 100
    option_radius = 40
    radius = Transmitter.radius
    small_option_radius = 20

    color = Config.blue_500
    preview_color = Config.blue_200

    def draw_option_image(self, image, rect):
        pygame.draw.circle(self.option_image, self.color,
                           rect.center, self.option_radius)
        image.blit(self.option_image, self.option_rect)

    def draw_small_option_image(self, image, rect):
        pygame.draw.circle(image, self.color, rect.center,
                           self.small_option_radius)

    def draw_preview_image(self):
        pygame.draw.circle(self._image, self.preview_color,
                           self.rect.center, self.radius)

    def draw_invalid_preview_image(self):
        pygame.draw.circle(self._image, self.invalid_preview_color,
                           self.rect.center, self.radius)


building_previews = {}
