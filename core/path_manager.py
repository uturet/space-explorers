
from game_objects.object_type import Building
from core.config import Config
import math
from collections import namedtuple
from core.property import EnergyInteraction


class PathManager:

    def __init__(self):
        self.consumers = set()
        self.producers = set()
        self.paths = {}  # {producer: {consumer: [[connection], [connection]]}}
        self.astart = AStar()

    def get_path(self, producer, consumer):
        return self.paths[producer][consumer]

    def add_building(self, building):
        if building.ei_type == Building.LATENT:
            self.update_paths()
        elif building.ei_type == Building.CONSUMER:
            self.add_consumer(building)
        elif building.ei_type == Building.PRODUCER:
            self.add_producer(building)

    def remove_building(self, building):
        self.remove_consumer(building)
        if building in self.producers:
            self.remove_producer(building)

    def remove_path_with_con(self, con):
        for producer in self.producers:
            for consumer in self.consumers:
                if (consumer in self.paths[producer] and
                        con in self.paths[producer][consumer]):
                    del self.paths[producer][consumer]
                    self.find_path(producer, consumer)

    def add_consumer(self, consumer):
        if consumer not in self.consumers:
            self.consumers.add(consumer)
            for producer in self.producers:
                self.find_path(producer, consumer)

    def remove_consumer(self, consumer):
        self.consumers.remove(consumer)
        for producer in self.producers:
            try:
                del self.paths[producer][consumer]
            except KeyError:
                pass

    def add_producer(self, producer):
        if producer not in self.producers:
            self.producers.add(producer)
            self.paths[producer] = {}
            for consumer in self.consumers:
                self.find_path(producer, consumer)

    def remove_producer(self, producer):
        self.producers.remove(producer)
        del self.paths[producer]

    def update_paths(self):
        for producer in self.producers:
            for consumer in self.consumers:
                self.find_path(producer, consumer)

    def find_path(self, producer, consumer):
        if producer == consumer:
            return
        path = self.astart.find_path(producer, consumer)
        if path:
            self.paths[producer][consumer] = path
            self.astart.clear()


VerticeWeight = namedtuple('VerticeWeight', 'g h f prev')


class AStar:
    def __init__(self):

        self.path_table = {}
        self.start_spr = None
        self.end_spr = None

    def find_path(self, start_spr, end_spr):
        opened = set()
        closed = set()
        self.start_spr = start_spr
        self.end_spr = end_spr
        cur_spr = start_spr

        opened.add(cur_spr)
        self.path_table[cur_spr] = VerticeWeight(
            *self.calculate_ghf(cur_spr),
            None
        )
        while cur_spr:
            for spr in cur_spr.building_con.keys():
                if (spr._ei_type != EnergyInteraction.PRODUCER and
                        spr not in closed):
                    opened.add(spr)
                    self.update_table(cur_spr, spr)

            closed.add(cur_spr)
            opened.remove(cur_spr)
            cur_spr = None
            for k, v in self.path_table.items():
                if k == end_spr:
                    return self.get_path()
                if k in closed or k._type == Building.PLAN:
                    continue
                if cur_spr is None:
                    cur_spr = k
                elif self.path_table[cur_spr].f > v.f:
                    cur_spr = k

        self.clear()

    def clear(self):
        self.path_table = {}

    def get_path(self):
        cons = set()
        prev_spr = self.end_spr
        while self.path_table[prev_spr].prev:
            cons.add(prev_spr.building_con[self.path_table[prev_spr].prev])
            prev_spr = self.path_table[prev_spr].prev
        return cons

    def calculate_ghf(self, next_spr):
        g = math.hypot(
            self.start_spr.rect.centerx - next_spr.rect.centerx,
            self.start_spr.rect.centery - next_spr.rect.centery)
        h = math.hypot(
            self.end_spr.rect.centerx - next_spr.rect.centerx,
            self.end_spr.rect.centery - next_spr.rect.centery)
        return g, h, g+h

    def update_table(self, prev_spr, next_spr):
        g, h, f = self.calculate_ghf(next_spr)
        if next_spr in self.path_table:
            if self.path_table[next_spr].f > f:
                self.path_table[next_spr] = VerticeWeight(g, h, f, prev_spr)
        else:
            self.path_table[next_spr] = VerticeWeight(g, h, f, prev_spr)
