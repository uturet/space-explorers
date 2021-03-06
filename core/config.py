import os
from static.colors import MaterialColors


class Config(MaterialColors):
    width = 1920
    height = 1080
    minimapwidth = 200
    minimapheight = 200
    hotbarwidth = 500
    hotbarheight = 100

    preview_cover_size = 200
    preview_cover_radius = 100

    mouse_tracker_width = 100
    mouse_tracker_height = 100

    bigmapwidth = 4000
    bigmapheight = 4000
    chunk_size = 100
    cornerpoint = [0, 0]
    fps = 60

    bg = (26, 35, 126)
    dark = (0, 0, 81)
    white = (255, 255, 255)
    red = (244, 67, 54)
    red_200 = (239, 154, 154)
    green = (0, 255, 0)
    blue = (33, 150, 243)
    blue_dark = (25, 118, 210)
    blue_light = (100, 181, 246)

    move_area = 0.02
    speed = 50
    scroll_speed = 100

    @classmethod
    def set_default_window_position(cls):
        x = 0
        y = 0
        os.environ['SDL_VIDEO_WINDOW_POS'] = f"{x},{y}"
