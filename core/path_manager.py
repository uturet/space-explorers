
from collections import deque
from game_objects.object_type import Building
from core.config import Config


class PathManager:
    consumers = {}  # {consumer: {producer: [path...]}}
    producers = {}
    visited = set()

    def add_building(self, building):
        if building.ei_type == Building.LATENT:
            self.update_paths()
        elif building.ei_type == Building.CONSUMER:
            self.add_consumer(building)
        elif building.ei_type == Building.PRODUCER:
            self.add_producer(building)
        self.visited.clear()

    def add_consumer(self, consumer):
        pass

    def remove_consumer(self, consumer):
        pass

    def add_producer(self, producer):
        self.producers[producer] = self.dfs(producer)

    def remove_producer(self, producer):
        pass

    def update_paths(self):
        for producer in self.producers:
            self.producers[producer] = self.dfs(producer)

    def find_path(self, building):
        has_end = False
        self.visited.add(building)
        paths = {}
        for con in building.building_con:
            path = deque()
            self.dfs(con, path, False)
            if path or has_end:
                has_end = False
                path.appendleft(con)
                if path[-1] not in paths:
                    paths[path[-1]] = []
                paths[path[-1]].append(path)
        return paths

    def dfs(self, building, path=None, entrypoint=True):
        self.visited.add(building)
        for con in building.building_con:
            if con.type == Building.CONSUMER:
                path.appendleft(con)
                return True
            if con in self.visited:
                continue
            if self.dfs(con, path, False):
                path.appendleft(con)
                return True
