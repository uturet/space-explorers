from core import collision_handler as ch
from core.config import Config
import pygame
import math


class Grid:

    __grid = {}

    def __init__(self):
        self._xlen = math.ceil(Config.bigmapwidth/Config.chunk_size)
        self._ylen = math.ceil(Config.bigmapheight/Config.chunk_size)
        for x in range(self._xlen+1):
            for y in range(self._ylen+1):
                self.__grid[f'{x}{y}'] = set()

    def add_item(self, item):
        chunk_indexes = {
            self._chunk(item.rect.topleft),
            self._chunk(item.rect.topright),
            self._chunk(item.rect.bottomleft),
            self._chunk(item.rect.bottomright)
        }
        for i in chunk_indexes:
            # TODO notify intersected
            self.__grid[i].add(item)

    def remove_item(self, item):
        chunk_indexes = {
            self._chunk(item.rect.topleft),
            self._chunk(item.rect.topright),
            self._chunk(item.rect.bottomleft),
            self._chunk(item.rect.bottomright)
        }
        for i in chunk_indexes:
            # TODO notify intersected
            self.__grid[i].remove(item)

    def move_item(self, item, new_pos):
        prev_chunk_indexes = {
            self._chunk(item.rect.topleft),
            self._chunk(item.rect.topright),
            self._chunk(item.rect.bottomleft),
            self._chunk(item.rect.bottomright)
        }
        item.rect.center = new_pos
        new_chunk_indexes = {
            self._chunk(item.rect.topleft),
            self._chunk(item.rect.topright),
            self._chunk(item.rect.bottomleft),
            self._chunk(item.rect.bottomright)
        }

        for i in (prev_chunk_indexes - new_chunk_indexes):
            # TODO notify intersected
            self.__grid[i].remove(item)

        for i in (new_chunk_indexes - prev_chunk_indexes):
            # TODO notify intersected
            self.__grid[i].add(item)

    def pos_intersects(self, pos, group):
        ch.get_rect_intersect_sprites_by_pos(
            pos, self.__grid[self._chunk(pos)], group)

    def rect_intersects(self, rect, group):
        left = math.ceil(max(0, rect.left) / Config.chunk_size)
        right = min(self._xlen+1,
                    max(0, math.ceil((rect.right / Config.chunk_size)+1)))
        top = math.ceil(max(0, rect.top) / Config.chunk_size)
        bottom = min(self._ylen+1,
                     max(0, math.ceil(rect.bottom / Config.chunk_size)+1))

        for x in range(left, right):
            for y in range(top, bottom):
                for item in self.__grid[f'{x}{y}']:
                    if rect.colliderect(item.rect):
                        group.add(item)

    def _chunk(self, pos):
        x = max(0, min(self._xlen, math.ceil(
            max(0, pos[0]) / Config.chunk_size)))
        y = max(0, min(self._ylen, math.ceil(
            max(0, pos[1]) / Config.chunk_size)))
        return f'{x}{y}'

    def draw_grid(self, image):
        for x in range(math.ceil(Config.bigmapwidth/Config.chunk_size)):
            for y in range(math.ceil(Config.bigmapheight/Config.chunk_size)):
                pygame.draw.rect(
                    image,
                    Config.amber_500,
                    (x*Config.chunk_size, y*Config.chunk_size,
                     Config.chunk_size, Config.chunk_size),
                    2
                )
