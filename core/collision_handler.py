import math
from user_interface.node import Node

COLLISION_TOLERANCE = 5


def get_circular_intersect_sprites_by_pos(pos, sprites, collisions):
    for sp in sprites:
        if math.hypot(pos[0] - sp.pos[0], pos[1] - sp.pos[1]) < sp.radius:
            collisions.add(sp)


def get_rect_intersect_sprites_by_pos(pos, sprites, collisions):
    for sp in sprites:
        if isinstance(sp, Node):
            coords = sp.calculate_abs_coords()
        else:
            coords = sp.rect
        if coords.left < pos[0] < coords.right and \
                coords.top < pos[1] < coords.bottom:
            collisions.add(sp)


def rect_collides(rect, sprites, collisions):
    for sp in sprites:
        if rect.colliderect(sp.rect):
            collisions.add(sp)


def circle_intersects_circle(pos_1, radius_1, pos_2, radius_2):
    return (math.hypot(pos_1[0] - pos_2[0], pos_1[1] - pos_2[1])) - (radius_1 + radius_2) < COLLISION_TOLERANCE
