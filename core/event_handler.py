import pygame
from ordered_set import OrderedSet


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
        self.mouse.pos = event.pos
        for handler in handlers:
            handler(self, event)

    def handle_defualt(self, handlers, event):
        for handler in handlers:
            handler(self, event)

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

    def register_handlers(self, sprite):
        for type, name in self.handler_names.items():
            if hasattr(sprite, name):
                self.register_handler(type, getattr(sprite, name))

    def remove_handler(self, type, handler):
        if type in self.handlers and handler in self.handlers[type]:
            self.handlers[type].remove(handler)

    def remove_handlers(self, sprite):
        for type, name in self.handler_names.items():
            if hasattr(sprite, name):
                self.remove_handler(type, getattr(sprite, name))

    def detect_handlers(self, sprites):
        for sp in sprites:
            self.register_handlers(sp)
