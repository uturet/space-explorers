

class Movement:
    speed = [0, 0]
    accel = [0, 0]

    def move(self, state):
        """Collision Detection"""
        new_pos = [self.rect.centerx, self.rect.centery]
        self.speed[0] += self.accel[0] * state.seconds
        new_pos[0] += self.speed[0] * state.seconds

        self.speed[1] += self.accel[1] * state.seconds
        new_pos[1] += self.speed[1] * state.seconds
        state.grid.move_item(self, new_pos)

    def handle_box_collision(self, box):
        """Discrete collision detection
            Sweep and Prune
            Space Partitions
                Uniform grid partition
                Smarter Space Partitioning
                    K-D Trees
            Object Partitions
                Bounding Volume Hierarchies
        """
        """Continuous collision detection"""
        if self.rect.left <= box.left or \
                self.rect.right >= box.right:
            self.speed[0] = -self.speed[0]
        if self.rect.bottom <= box.bottom or \
                self.rect.top >= box.top:
            self.speed[1] = -self.speed[1]


class EnergyInteraction:
    LATENT = 0
    CONSUMER = 1
    PRODUCER = 2
    _ei_type = LATENT

    @property
    def ei_type(self):
        return self._ei_type

    @ei_type.setter
    def ei_type(self, i):
        if i in (self.LATENT, self.CONSUMER, self.PRODUCER):
            self._ei_type = i
        else:
            raise Exception(
                f'Invalid {self.__class__.__name___}.type. Should be one of {",".join(self.LATENT, self.CONSUMER, self.PRODUCER)}, given {i}')
