from user_interface import Node
from core.config import Config


class Button(Node):
    width = 30
    height = 30
    is_acitve = False

    def __init__(
            self, parent, mod_index, on_mousedown=None,
            on_mouseup=None, color=Config.blue_500):
        Node.__init__(self, parent)
        self.color = color
        self.mod_index = mod_index
        self.on_mousedown = None
        self.on_mouseup = None
        if on_mousedown:
            self.on_mousedown = on_mousedown
        if on_mouseup:
            self.on_mouseup = on_mouseup

        self.rect.topleft = (0, 0)
        self.paintbtn()

    def paintbtn(self):
        self.image.fill(self.color)

    def handle_mousebuttonup(self, state, event):
        if (self in state.mouse_intersected and self.on_mouseup and
                state.hotbar.active_mod_index == self.mod_index):
            self.on_mouseup(state, event)

    def handle_mousebuttondown(self, state, event):
        if (self in state.mouse_intersected and self.on_mousedown and
                state.hotbar.active_mod_index == self.mod_index):
            self.on_mousebuttondown(state, event)
