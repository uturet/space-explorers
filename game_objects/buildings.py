import pygame
from game_objects.object_types import Building
from core.config import Config


class Transmitter(Building):
    coverage_radius = 100
    size = 20
    radius = 10
    color = Config.blue_500
    hover_color = Config.blue_200
    active_color = Config.green_200

    option_radius = 40
    preview_color = Config.blue_200

    def __init__(self, pos):
        super().__init__(pos)
        self.paint()

    def paint(self):
        pygame.draw.circle(
            self._image,
            self.color,
            (self.radius, self.radius),
            self.radius
        )

        if self.is_hover and not self.is_active:
            pygame.draw.circle(
                self._image,
                self.hover_color,
                (self.radius, self.radius),
                self.radius,
                2
            )
        if self.is_active:
            pygame.draw.circle(
                self._image,
                self.active_color,
                (self.radius, self.radius),
                self.radius,
                2
            )

        self.image = self._image.convert_alpha()

    def update(self, state):
        pass

    def handle_mousebuttonup(self, state, event):
        if self in state.mouse_int_sprites:
            self.is_active = True
            self.paint()
        elif self.is_active:
            self.is_active = False
            self.paint()

    def handle_mousemotion(self, state, event):
        if self in state.mouse_int_sprites:
            self.is_hover = True
            self.paint()
        elif self.is_hover:
            self.is_hover = False
            self.paint()

    @classmethod
    def get_option_image(cls):
        image = pygame.Surface(
            (Config.building_selector_height, Config.building_selector_height),
            pygame.SRCALPHA)
        rect = image.get_rect()
        pygame.draw.circle(image, cls.color, rect.center, cls.option_radius)

        return image

    @classmethod
    def get_preview_image(cls):
        image = pygame.Surface(
            (Config.mouse_tracker_width, Config.mouse_tracker_height),
            pygame.SRCALPHA)
        rect = image.get_rect()
        pygame.draw.circle(image, cls.preview_color,
                           rect.center, cls.radius)
        return image


buildings = (
    Transmitter,
)
