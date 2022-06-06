from core.event_handler import EventHandler


class LiveCicleManager(EventHandler):

    def create_gameobj(self, cls, *args, **kwargs):
        obj = cls(*args, **kwargs)
        self.register_handlers(obj)

    def remove_gameobj(self, obj):
        for g in obj.groups:
            g.remove(obj)
        self.remove_handlers(obj)
