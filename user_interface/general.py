from user_interface import Node
from core.config import Config


class Button(Node):
    width = 50
    height = 50
    color = Config.blue_500

    def __init__(self, parent):
        Node.__init__(self, parent)
        self.rect.topleft = (0, 0)
        self.paintbtn()

    def paintbtn(self):
        self.image.fill(self.color)
