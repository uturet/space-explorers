from game_objects.object_type import Building
from user_interface.hotbar import ControlBar
from user_interface import Node
from game_objects.buildings import building_previews
from core.config import Config


class InfoBar(Node):
    width = Config.hotbarwidth
    height = Config.hotbarheight

    def __init__(self, parent):
        super().__init__(parent)
        self.infobar_preview = InfobarPreview(self)
        self.control_bar = ControlBar(
            self, self.width,
            self.height, self.infobar_preview.rect.w)

    def set_info_provider(self, sprite):
        self.control_bar.set_info_provider(sprite)
        sprite.set_ui_type(Building.SELECTED)
        building_previews[sprite.__class__.__name__].draw_option_image(
            self.infobar_preview.rect.center, self.infobar_preview.image)
        self.image.blit(self.infobar_preview.image, self.infobar_preview.rect)
        self.image.blit(self.control_bar.image, self.control_bar.rect)


class InfobarPreview(Node):
    width = InfoBar.height
    height = InfoBar.height
