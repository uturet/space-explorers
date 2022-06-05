from config import Config


class Mouse:
    pos = (Config.width/2, Config.height/2)

    def __init__(self, bg):
        self._bg = bg

    @property
    def pos_x(self):
        x = round(
            self.pos[0] - (self._bg.pos[0] - (self._bg.dimens[0]/2)))
        return max(0, min(x, self._bg.dimens[0]))

    @property
    def pos_y(self):
        y = round(
            self.pos[1] - (self._bg.pos[1] - (self._bg.dimens[1]/2)))
        return max(0, min(y, self._bg.dimens[1]))

    @property
    def bg_bos(self):
        return (self.pos_x, self.pos_y)
