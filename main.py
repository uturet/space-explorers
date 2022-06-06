import pygame
from core.config import Config
from core.state import State

Config.set_default_window_position()


class Game:

    def __init__(self):
        pygame.init()
        self.state = State()

    def main_loop(self):
        running = True
        while running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                self.state.handle_event(event)
            self.state.update()
            self.draw()
        pygame.quit()

    def draw(self):
        pygame.display.set_caption(str(self.state.clock.get_fps()))
        pygame.display.flip()
        self.state.clock.tick(Config.fps)


if __name__ == "__main__":
    g = Game()
    g.main_loop()
