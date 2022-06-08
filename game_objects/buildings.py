import pygame
from game_objects.object_types import Building, Preview
from core.config import Config
from core.property import Movement


class Transmitter(Building, Movement):
    speed = [0, 0]
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

        if self.is_hover and not self.is_active:
            pygame.draw.circle(self._image, self.hover_color,
                               (self.radius, self.radius), self.radius, 2
                               )
        if self.is_active:
            pygame.draw.circle(self._image, self.active_color,
                               (self.radius, self.radius), self.radius, 2
                               )

        self.image = self._image.convert_alpha()

    def update(self, state):
        self.move(state)
        self.handle_box_collision(state.bg.box)

    def handle_mousebuttonup(self, state, event):
        if self in state.mouse_intersected:
            self.is_active = True
            self.paint()
        elif self.is_active:
            self.is_active = False
            self.paint()

    def handle_mousemotion(self, state, event):
        if self in state.mouse_intersected:
            self.is_hover = True
            self.paint()
        elif self.is_hover:
            self.is_hover = False
            self.paint()


class TransmitterPreview(Preview):
    building = Transmitter

    cover_size = 200
    cover_radius = 100
    radius = Transmitter.radius
    option_radius = 40

    color = Config.blue_500
    preview_color = Config.blue_200

    def draw_option_image(self, image, rect):
        pygame.draw.circle(image, self.color, rect.center, self.option_radius)

    def draw_preview_image(self,):
        pygame.draw.circle(self.preview_image, self.preview_color,
                           self.preview_rect.center, self.radius)


building_previews = (
    TransmitterPreview,
)
