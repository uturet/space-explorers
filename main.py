import pygame
from config import Config
from state import State
from seeder import seed_players_rand

Config.set_default_window_position()
state = State()


class EventHandler():

    handlers = {
        pygame.MOUSEMOTION: set(),
        pygame.MOUSEBUTTONDOWN: set(),
        pygame.MOUSEBUTTONUP: set()
    }

    def mousemotion_handler(self, event):
        if event.type == pygame.MOUSEMOTION:
            state.mouse.pos = event.pos
            for handler in self.handlers[pygame.MOUSEMOTION]:
                handler(state, event)

    def mousebuttondown_handler(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for handler in self.handlers[pygame.MOUSEBUTTONDOWN]:
                handler(state, event)

    def mousebuttonup_handler(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            for handler in self.handlers[pygame.MOUSEBUTTONUP]:
                handler(state, event)

    def register_handler(self, type, handler):
        if type in self.handlers:
            self.handlers[type].add(handler)

    def remove_handler(self, type, handler):
        if type in self.handlers and handler in self.handlers[type]:
            self.handlers[type].remove(handler)


class Game(EventHandler):

    def __init__(self):
        pygame.init()

        self.register_handler(pygame.MOUSEMOTION, state.bg.hanlde_mausemotion)
        self.register_handler(pygame.MOUSEBUTTONDOWN,
                              state.radarmap.handle_mousebuttondown)
        self.register_handler(pygame.MOUSEBUTTONUP,
                              state.radarmap.handle_mousebuttonup)
        self.register_handler(pygame.MOUSEMOTION,
                              state.radarmap.handle_mousemotion)

    def main_loop(self):

        seed_players_rand(10, state)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                self.mousemotion_handler(event)
                self.mousebuttondown_handler(event)
                self.mousebuttonup_handler(event)

            state.update()

            self.draw()

        pygame.quit()

    def draw(self):
        pygame.display.set_caption(str(state.clock.get_fps()))
        pygame.display.flip()
        state.clock.tick(Config.fps)


if __name__ == "__main__":
    g = Game()
    g.main_loop()
