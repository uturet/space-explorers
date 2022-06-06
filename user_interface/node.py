from collections import namedtuple
Coords = namedtuple('Coords', 'left top right bottom')


class Node:

    def __init__(self, parent):
        self.parent = parent

    def calculate_abs_coords(self, parent=None, coords=None):
        enter = False
        if not coords:
            enter = True
            parent = self.parent
            coords = {
                'left': self.rect.left,
                'top': self.rect.top,
                'right': self.rect.right,
                'bottom': self.rect.bottom,
            }

        if parent:
            coords['left'] += parent.rect.left
            coords['top'] += parent.rect.top
            coords['right'] += parent.rect.left
            coords['bottom'] += parent.rect.top
            self.calculate_abs_coords(parent.parent, coords)
        if enter:
            return Coords(**coords)
