from user_interface.hotbar import HotbarMod, ControlBar
from user_interface import Node
from game_objects.buildings import building_previews


class InfoBar(HotbarMod):

    def __init__(self, parent):
        super().__init__(parent)
        self.infobar_preview = InfobarPreview(self)
        self.control_bar = ControlBar(
            self, self.width, self.height, self.infobar_preview.rect.w)

    def set_info_provider(self, sprite):
        self.control_bar.info_provider = sprite
        building_previews[sprite.__class__.__name__].draw_option_image(
            self.infobar_preview.image, self.infobar_preview.rect)
        self.image.blit(self.infobar_preview.image, self.infobar_preview.rect)
        self.image.blit(self.control_bar.image, self.control_bar.rect)


class InfobarPreview(Node):
    width = InfoBar.height
    height = InfoBar.height
