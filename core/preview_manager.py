import pygame
from core.config import Config
from collections import namedtuple
import math


class ConnectionPreview(pygame.sprite.Sprite):
    groups = ()

    def __init__(self, image, rect, mask):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = image
        self.rect = rect
        self.mask = mask


class PreviewManager:

    def __init__(self):
        self.height = 4
        self.width = 100
        self.colors = ()
        self.frames = {}  # {angle: {distance: ConnectionPreview}}
        self.step = 3
        self.covered = {}  # {angle: [distance, opp, spr, opp]}
        self.exclede_angles = {}  # {distance: [[angle, ...], [angle, ...]]}
        self.dis_anlge = {
            10: round(45/self.step),
            20: round(27/self.step),
            30: round(19/self.step),
            40: round(14/self.step),
            50: round(12/self.step),
            60: round(10/self.step),
            70: round(8/self.step),
            80: round(7/self.step),
            90: round(6/self.step),
            100: round(6/self.step),
        }

        colors = (
            Config.orange_500,
            Config.red_500,
            Config.green_500,
            Config.indigo_500,
            Config.teal_500,
            Config.orange_500,
            Config.red_500,
            Config.green_500,
            Config.indigo_500,
            Config.teal_500,
        )
        for i, color in enumerate(colors):
            self.create_frames(self.width-(i*10), color)

    def create_frames(self, width, color):
        for angle in range(0, 360, self.step):
            if angle not in self.frames:
                self.frames[angle] = {}
            converted = self.create_frame(width, angle, color)
            rect = converted.get_rect()
            if angle == 0:
                rect.topleft = (self.width, self.width)
                rect.top -= self.height/2
            elif angle < 90:
                rect.bottomleft = (self.width, self.width)
            elif angle == 90:
                rect.bottomleft = (self.width, self.width)
                rect.left -= self.height/2
            elif angle < 180:
                rect.bottomright = (self.width, self.width)
            elif angle == 180:
                rect.bottomright = (self.width, self.width)
                rect.top += self.height/2
            elif angle < 270:
                rect.topright = (self.width, self.width)
            elif angle == 270:
                rect.topright = (self.width, self.width)
                rect.right += self.height/2
            else:
                rect.topleft = (self.width, self.width)
            con = ConnectionPreview(
                converted, rect, pygame.mask.from_surface(converted))
            self.frames[angle][width] = con

    def create_frame(self, width, angle, color):
        image = pygame.Surface(
            (width, self.height), pygame.SRCALPHA)
        rect = image.get_rect()
        pygame.draw.line(image, color,
                         rect.midleft, rect.midright, self.height)
        converted = image.convert_alpha()
        converted = pygame.transform.rotate(converted, angle)
        return converted

    # def draw(self, image):
    #     for frame in self.images:
    #         image.blit(frame.image, frame.rect.topleft)

    def set_connections(self, state, intersections):
        self.covered.clear()
        for spr in intersections:
            self.save_sprite(state.mouse.rect.center, spr)
        state.tmp_preview_group.update(self.validate_by_mask())

    def get_connection(self, angle, distance, pos):
        if angle == 0:
            self.frames[angle][distance].rect.topleft = pos
            self.frames[angle][distance].rect.top -= self.height/2
        elif angle < 90:
            self.frames[angle][distance].rect.bottomleft = pos
        elif angle == 90:
            self.frames[angle][distance].rect.bottomleft = pos
            self.frames[angle][distance].rect.left -= self.height/2
        elif angle < 180:
            self.frames[angle][distance].rect.bottomright = pos
        elif angle == 180:
            self.frames[angle][distance].rect.bottomright = pos
            self.frames[angle][distance].rect.top += self.height/2
        elif angle < 270:
            self.frames[angle][distance].rect.topright = pos
        elif angle == 270:
            self.frames[angle][distance].rect.topright = pos
            self.frames[angle][distance].rect.right += self.height/2
        else:
            self.frames[angle][distance].rect.topleft = pos
        return self.frames[angle][distance]

    def save_sprite(self, start_pos, spr):
        y_cat = start_pos[1] - spr.rect.center[1]
        x_cat = start_pos[0] - spr.rect.center[0]
        hypot = math.hypot(x_cat, y_cat)
        sign = ''
        if ((y_cat < 0 and x_cat < 0) or (y_cat > 0 and x_cat > 0)):
            angle = self.step * \
                int(math.degrees(math.acos(abs(y_cat)/hypot))/(self.step))
            sign = 'cos'
            angle = 90 + abs(angle)
            if y_cat <= 0:
                angle = 180 + angle
        else:
            angle = self.step * \
                int(math.degrees(math.asin(abs(y_cat)/hypot))/(self.step))
            sign = 'sin'
            if y_cat < 0 or x_cat > 0:
                angle = 180 + abs(angle)
        distance = 10 * int(hypot / 10)
        if distance > 100:
            return
        cover_angles = [angle]
        [cover_angles.append(a) for a in range(
            angle-self.dis_anlge[distance], angle+self.dis_anlge[distance]+1)]
        ca_set = set(cover_angles)
        rm_ex = None
        for ex_dis, points in self.exclede_angles.items():
            for i, angles in enumerate(points):
                if angle in angles:
                    if ex_dis < distance:
                        return
                    else:
                        rm_ex = (ex_dis, i)
                        del self.covered[angles[0]]
                if (ex_dis > distance and ca_set.intersection(angles)):
                    rm_ex = (ex_dis, i)
                    del self.covered[angles[0]]
        if rm_ex:
            del self.exclede_angles[rm_ex[0]][rm_ex[1]]

        self.covered[angle] = [
            distance, spr, self.get_connection(angle, distance, start_pos)
        ]

    def validate_by_mask(self):
        connectoins = set()
        invalid = set()

        if len(self.covered) == 1:
            return [list(self.covered.values())[0][2]]

        for angle_1, data_1 in self.covered.items():
            for angle_2, data_2 in self.covered.items():
                if angle_1 == angle_2 or data_1[2] in invalid:
                    continue
                if (angle_1-45 < angle_2 > angle_1+45):
                    if not pygame.sprite.collide_mask(data_1[1], data_2[2]):
                        connectoins.add(data_2[2])
                    else:
                        invalid.add(data_2[2])
        return connectoins
