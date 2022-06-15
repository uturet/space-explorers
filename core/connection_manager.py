import pygame
from core.config import Config
import math
from core.animation import Frame


class ConnectionPreview(pygame.sprite.Sprite):
    groups = ()

    def __init__(self, angle, distance, image, rect, mask):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = image
        self.rect = rect
        self.mask = mask
        self.angle = angle
        self.distance = distance

    def create_connection(self, state, con_from, con_to):
        frames = []
        for color in Connection.colors:
            f = Frame(*state.connection_manager.create_frame(
                self.distance, self.angle, color, con_from.rect.center
            ))
            frames.append(f)

        return Connection(con_from, con_to, frames)


class ConnectionManager:
    cover_size = Config.preview_cover_size
    cover_radius = Config.preview_cover_radius

    def __init__(self):
        self.height = 4
        self.width = self.cover_radius
        self.color = Config.bluegrey_200
        self.frames = {}  # {angle: {distance: ConnectionPreview}}
        self.step = 2
        self.covered = {}  # {angle: [distance, opp, spr, opp]}
        for i in range(10):
            self.create_frames(self.width-(i*10), self.color)

    def create_frames(self, distance, color):
        for angle in range(0, 360, self.step):
            if angle not in self.frames:
                self.frames[angle] = {}
            image, rect, mask = self.create_frame(distance, angle, color)
            con = ConnectionPreview(
                angle, distance, image, rect, mask)
            self.frames[angle][distance] = con

    def create_frame(self, distance, angle, color, pos=None):
        image = self.create_image(distance, angle, color)
        rect = image.get_rect()
        if not pos:
            pos = (self.width, self.width)
        self.set_default_pos(angle, rect, pos)
        mask = pygame.mask.from_surface(image)
        return image, rect, mask

    def set_default_pos(self, angle, rect, pos):
        if angle == 0:
            rect.topleft = pos
            rect.top -= self.height/2
        elif angle < 90:
            rect.bottomleft = pos
        elif angle == 90:
            rect.bottomleft = pos
            rect.left -= self.height/2
        elif angle < 180:
            rect.bottomright = pos
        elif angle == 180:
            rect.bottomright = pos
            rect.top += self.height/2
        elif angle < 270:
            rect.topright = pos
        elif angle == 270:
            rect.topright = pos
            rect.right += self.height/2
        else:
            rect.topleft = pos

    def create_image(self, width, angle, color):
        image = pygame.Surface(
            (width, self.height), pygame.SRCALPHA)
        rect = image.get_rect()
        pygame.draw.line(image, color,
                         rect.midleft, rect.midright, self.height)
        converted = image.convert_alpha()
        converted = pygame.transform.rotate(converted, angle)
        return converted

    def set_connections(self, state, intersections):
        self.covered.clear()
        for spr in intersections:
            self.save_point(state.mouse.bg_rect.center, spr)
        self.validate_by_mask(state.tmp_preview_group)

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

    def save_point(self, start_pos, spr):
        y_cat = start_pos[1] - spr.rect.center[1]
        x_cat = start_pos[0] - spr.rect.center[0]
        hypot = math.hypot(x_cat, y_cat)
        if ((y_cat < 0 and x_cat < 0) or (y_cat > 0 and x_cat > 0)):
            angle = self.step * \
                int(math.degrees(math.acos(abs(y_cat)/hypot))/(self.step))
            angle = 90 + abs(angle)
            if y_cat <= 0:
                angle = 180 + angle
        else:
            angle = self.step * \
                int(math.degrees(math.asin(abs(y_cat)/hypot))/(self.step))
            if y_cat < 0 or x_cat > 0:
                angle = 180 + abs(angle)
        distance = 10 * int(hypot / 10)
        if distance > 100:
            return
        if distance == 0:
            return
        if angle in self.covered:
            if self.covered[angle][0] > distance:
                self.covered[angle] = [
                    distance, spr, self.get_connection(
                        angle, distance, start_pos)]
        else:
            self.covered[angle] = [
                distance, spr, self.get_connection(angle, distance, start_pos)
            ]

    def validate_by_mask(self, building_con):
        connectoins = {}
        invalid = set()

        if len(self.covered) == 1:
            point = list(self.covered.values())[0]
            building_con[point[1]] = point[2]

        for angle_1, data_1 in self.covered.items():
            for angle_2, data_2 in self.covered.items():
                if angle_1 == angle_2 or data_1[1] in invalid:
                    continue
                left = angle_1-45
                if left < 0:
                    left += 360
                right = angle_1+45
                if right > 360:
                    right -= 360
                if (left < angle_2 or angle_2 < right):
                    con = pygame.sprite.collide_mask(data_1[1], data_2[2])
                    if not con:
                        connectoins[data_2[1]] = data_2[2]
                    else:
                        invalid.add(data_2[1])
                        connectoins[data_1[1]] = data_1[2]
                else:
                    connectoins[data_2[1]] = data_2[2]
        for spr in connectoins.keys() - invalid:
            building_con[spr] = connectoins[spr]


class Connection(pygame.sprite.Sprite):
    groups = ()
    colors = (Config.lightblue_500, Config.orange_500)
    connects = None

    def __init__(self, start_spr, end_spr, frames):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.connects = {start_spr, end_spr}
        self.frames = frames
        self.select_frame(0)

    def select_frame(self, index):
        self.image = self.frames[index].image
        self.rect = self.frames[index].rect
        self.mask = self.frames[index].mask

    def activate(self):
        self.select_frame(1)

    def deactivate(self):
        self.select_frame(0)
