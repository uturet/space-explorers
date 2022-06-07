import pygame
from game_objects.object_types import Building, Preview
from core.config import Config
from core import collision_handler as ch


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
        pass

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

    lines = set()

    def get_option_image(self):
        image = pygame.Surface(
            (Config.building_selector_height, Config.building_selector_height),
            pygame.SRCALPHA)
        rect = image.get_rect()
        pygame.draw.circle(image, self.color, rect.center, self.option_radius)
        return image

    def get_preview_image(self):
        image = pygame.Surface(
            (self.cover_size, self.cover_size),
            pygame.SRCALPHA)
        return image

    def update_preview_image(self):
        self.preview_image.fill((255, 255, 255, 0))
        for line_args in self.lines:
            pygame.draw.line(*line_args)
        pygame.draw.circle(self.preview_image, self.preview_color,
                           self.preview_rect.center, self.radius)

    def handle_collisions(self, state, collisions):
        self.lines.clear()
        for sp in collisions:
            if isinstance(sp, self.building) and \
                ch.circle_intersects_circle(
                    state.mouse.bg_pos, self.cover_radius,
                    sp.rect.center, sp.radius
            ):
                pos = state.mouse.bg_pos_to_abs(sp.rect.center)
                pos = (
                    pos[0]-state.mouse.pos[0]+self.preview_rect.centerx,
                    pos[1]-state.mouse.pos[1]+self.preview_rect.centery
                )
                self.lines.add(
                    (
                        self.preview_image,
                        self.color,
                        self.preview_rect.center,
                        pos,
                        3
                    )
                )


building_previews = (
    TransmitterPreview,
)
