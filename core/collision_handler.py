from user_interface.node import Node
import pygame
import math

COLLISION_TOLERANCE = 5


def get_circular_intersect_sprites_by_pos(pos, sprites, collisions):
    for sp in sprites:
        if math.hypot(pos[0] - sp.pos[0], pos[1] - sp.pos[1]) < sp.radius:
            collisions.add(sp)


def get_rect_intersect_sprites_by_pos(pos, sprites, collisions):
    for sp in sprites:
        if sp.rect.left < pos[0] < sp.rect.right and \
                sp.rect.top < pos[1] < sp.rect.bottom:
            collisions.add(sp)


def is_pos_intersects_rect(pos, rect):
    return (rect.left < pos[0] < rect.right and
            rect.top < pos[1] < rect.bottom)


def rect_collides(rect, sprites, collisions):
    for sp in sprites:
        if rect.colliderect(sp.rect):
            collisions.add(sp)


def circle_intersects_circle(pos_1, radius_1, pos_2, radius_2):
    return (math.hypot(pos_1[0] - pos_2[0], pos_1[1] - pos_2[1])) - (radius_1 + radius_2) < COLLISION_TOLERANCE


def rect_from_points(pos1, pos2):
    rect = ['l', 't', 'w', 'h']
    if pos1[0] < pos2[0]:
        rect[0] = pos1[0]
        rect[2] = pos2[0] - rect[0]
    else:
        rect[0] = pos2[0]
        rect[2] = pos1[0] - rect[0]
    if pos1[1] < pos2[1]:
        rect[1] = pos1[1]
        rect[3] = pos2[1] - rect[1]
    else:
        rect[1] = pos2[1]
        rect[3] = pos1[1] - rect[1]
    return pygame.Rect(rect)
