import pygame
from core.config import Config
from core.state import State
Config.set_default_window_position()


class Game:

    def __init__(self):
        pygame.init()
        self.state = State()
        self.clock = pygame.time.Clock()
        pygame.font.init()

    def main_loop(self):
        running = True
        while running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                self.state.event_manager.notify(event)

            for tmp_sub in self.state.tmp_event_group:
                for event in events:
                    if hasattr(event, 'pos'):
                        event.pos = self.state.bg.abs_pos_to_bg(*event.pos)
                    self.state.event_manager.notify_tmp_sub(tmp_sub, event)

            self.state.update()
            self.draw()
        pygame.quit()

    def draw(self):
        pygame.display.set_caption(str(round(self.clock.get_fps())))
        pygame.display.flip()
        self.state.milliseconds = self.clock.tick(Config.fps)
        self.state.seconds = self.state.milliseconds / 1000.0


if __name__ == "__main__":
    g = Game()
    g.main_loop()
