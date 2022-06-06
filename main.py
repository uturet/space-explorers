import pygame
from config import Config
from state import State
from seeder import seed_players_rand
from ordered_set import OrderedSet

Config.set_default_window_position()
state = State()


class EventHandler():

    handlers = {
        pygame.MOUSEMOTION: OrderedSet(),
        pygame.MOUSEBUTTONDOWN: OrderedSet(),
        pygame.MOUSEBUTTONUP: OrderedSet(),
        pygame.MOUSEWHEEL: OrderedSet(),
    }

    handler_names = {
        pygame.MOUSEMOTION: 'handle_mousemotion',
        pygame.MOUSEBUTTONDOWN: 'handle_mousebuttondown',
        pygame.MOUSEBUTTONUP: 'handle_mousebuttonup',
        pygame.MOUSEWHEEL: 'handle_mousewheel',
    }

    def handle_mousemotion(self, handlers, event):
        state.mouse.pos = event.pos
        for handler in handlers:
            handler(state, event)

    def handle_defualt(self, handlers, event):
        for handler in handlers:
            handler(state, event)

    def handle_event(self, event):
        for type in self.handlers:
            if event.type == type:
                if not hasattr(self, self.handler_names[type]):
                    self.handle_defualt(self.handlers[type], event)
                    continue
                getattr(self, self.handler_names[type])(
                    self.handlers[type], event)

    def register_handler(self, type, handler):
        if type in self.handlers:
            self.handlers[type].add(handler)

    def remove_handler(self, type, handler):
        if type in self.handlers and handler in self.handlers[type]:
            self.handlers[type].remove(handler)

    def detect_handlers(self, sprites):
        for type, name in self.handler_names.items():
            for sp in sprites:
                if hasattr(sp, name):
                    self.register_handler(type, getattr(sp, name))


class Game(EventHandler):

    def __init__(self):
        pygame.init()
        self.detect_handlers(state.uigroup)
        self.detect_handlers(state.interactable_group)

    def main_loop(self):

        seed_players_rand(10, state)

        running = True
        while running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False

                self.handle_event(event)

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
