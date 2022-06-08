

class Movement:
    speed = [0, 0]
    accel = [0, 0]

    def move(self, state):
        """Collision Detection"""
        new_pos = [self.rect.centerx, self.rect.centery]
        dt = state.clock.get_time() / 1000
        self.speed[0] += self.accel[0] * dt
        new_pos[0] += self.speed[0] * dt

        self.speed[1] += self.accel[1] * dt
        new_pos[1] += self.speed[1] * dt
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
        # if self.left[0] <= box.left[0] or \
        #         self.right[0] >= box.right[0]:
        #     self.speed[0] = -self.speed[0]
        # if self.bottom[1] <= box.bottom[1] or \
        #         self.top[1] >= box.top[1]:
        #     self.speed[1] = -self.speed[1]
        if self.rect.left <= box.left or \
                self.rect.right >= box.right:
            self.speed[0] = -self.speed[0]
        if self.rect.bottom <= box.bottom or \
                self.rect.top >= box.top:
            self.speed[1] = -self.speed[1]
