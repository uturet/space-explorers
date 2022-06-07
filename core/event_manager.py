import pygame
from ordered_set import OrderedSet


class EventManager:

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

    def __init__(self, state):
        self.state = state

    def notify(self, event):
        for type in self.handlers:
            if event.type == type:
                for handler in self.handlers[type]:
                    handler(self.state, event)

    def notify_tmp_sub(self, subscriber, event):
        for type, name in self.handler_names.items():
            if event.type == type:
                if hasattr(subscriber, name):
                    getattr(subscriber, name)(self.state, event)

    def add_subscriber(self, subscriber):
        for type, name in self.handler_names.items():
            if hasattr(subscriber, name):
                if type in self.handlers:
                    self.handlers[type].add(getattr(subscriber, name))

    def remove_subscriber(self, subscriber):
        for type, name in self.handler_names.items():
            if hasattr(subscriber, name):
                if type in self.handlers and \
                        getattr(subscriber, name) in self.handlers[type]:
                    self.handlers[type].remove(getattr(subscriber, name))

    def add_group(self, *group):
        for sub in group:
            self.add_subscriber(sub)

    def remove_group(self, group):
        for sub in group:
            self.add_subscriber(sub)
