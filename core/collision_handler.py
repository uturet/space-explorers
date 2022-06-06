import math
from user_interface import Node


class CollisionHandler:
    def get_circular_intersect_sprites_by_pos(self, pos, sprites):
        for sp in sprites:
            if math.hypot(pos[0] - sp.pos[0], pos[1] - sp.pos[1]) < sp.radius:
                self.mouse_int_sprites.add(sp)

    def get_rect_intersect_sprites_by_pos(self, pos, sprites):
        for sp in sprites:
            if isinstance(sp, Node):
                coords = sp.calculate_abs_coords()
            else:
                coords = sp.rect
            if coords.left < pos[0] < coords.right and \
                    coords.top < pos[1] < coords.bottom:
                self.mouse_int_sprites.add(sp)

    def calculate_mouse_int_sprites(self):
        self.mouse_int_sprites.clear()
        self.get_rect_intersect_sprites_by_pos(
            self.mouse.pos,
            self.uigroup
        )
        self.get_rect_intersect_sprites_by_pos(
            self.mouse.pos,
            self.interactable_group
        )
        self.get_rect_intersect_sprites_by_pos(
            self.mouse.pos,
            self.gamegroup
        )
