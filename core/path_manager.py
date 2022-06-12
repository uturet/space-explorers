
from collections import deque
from game_objects.object_type import Building
from core.config import Config


class PathManager:
    consumers = {}  # {consumer: {producer: [path...]}}
    producers = {}
    visited = set()

    def add_building(self, building):
        if building.type == Building.LATENT:
            self.update_paths()
        elif building.type == Building.CONSUMER:
            self.add_consumer(building)
        elif building.type == Building.PRODUCER:
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

    def dfs(self, building, path=None, entrypoint=True):
        has_end = False
        if entrypoint:
            self.visited.add(building)
            paths = {}
        for con in building.building_con:
            if con.type == Building.CONSUMER:
                path.appendleft(con)
                has_end = True
            if con in self.visited:
                continue
            self.visited.add(con)
            if entrypoint:
                path = deque()
                self.dfs(con, path, False)
                if path or has_end:
                    has_end = False
                    path.appendleft(con)
                    if path[-1] not in paths:
                        paths[path[-1]] = []
                    paths[path[-1]].append(path)
            elif not has_end:
                if self.dfs(con, path, False):
                    path.appendleft(con)
                    return True
        if entrypoint:
            return paths
        return has_end
