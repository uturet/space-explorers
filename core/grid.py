from core.config import Config
import math
from core import collision_handler as ch


class Grid:

    __grid = {}

    def __init__(self):
        for x in range(math.ceil(Config.bigmapwidth/Config.chunk_size)):
            for y in range(math.ceil(Config.bigmapheight/Config.chunk_size)):
                self.__grid[f'{x}{y}'] = set()

    def add_item(self, item):
        chunk_indexes = set(
            self._chunk(item.rect.topleft),
            self._chunk(item.rect.topright),
            self._chunk(item.rect.bottomleft),
            self._chunk(item.rect.bottomright)
        )
        for i in chunk_indexes:
            # TODO notify intersected
            self.__grid[i].add(item)

    def remove_item(self, item):
        chunk_indexes = set(
            self._chunk(item.rect.topleft),
            self._chunk(item.rect.topright),
            self._chunk(item.rect.bottomleft),
            self._chunk(item.rect.bottomright)
        )
        for i in chunk_indexes:
            # TODO notify intersected
            self.__grid[i].remove(item)

    def move_item(self, item, new_pos):
        prev_chunk_indexes = set(
            self._chunk(item.rect.topleft),
            self._chunk(item.rect.topright),
            self._chunk(item.rect.bottomleft),
            self._chunk(item.rect.bottomright)
        )
        item.rect.center = new_pos
        new_chunk_indexes = set(
            self._chunk(item.rect.topleft),
            self._chunk(item.rect.topright),
            self._chunk(item.rect.bottomleft),
            self._chunk(item.rect.bottomright)
        )

        for i in (prev_chunk_indexes - new_chunk_indexes):
            # TODO notify intersected
            self.__grid[i].remove(item)

        for i in (new_chunk_indexes - prev_chunk_indexes):
            # TODO notify intersected
            self.__grid[i].add(item)

    def pos_intersects(self, pos, group):
        ch.get_rect_intersect_sprites_by_pos(
            pos, self.__grid[self._chunk(pos)], group)

    def pos_intersects_by_rect(self, rect, group):
        chunk_indexes = set(
            self._chunk(rect.topleft),
            self._chunk(rect.topright),
            self._chunk(rect.bottomleft),
            self._chunk(rect.bottomright)
        )
        for i in chunk_indexes:
            for item in self.__grid[i]:
                if rect.colliderect(item.rect):
                    group.add(item)

    @staticmethod
    def _chunk(pos):
        return f'{math.ceil(pos[0] / Config.chunk_size)}{math.ceil(pos[1] / Config.chunk_size)}'
