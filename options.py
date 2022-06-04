import os


class Options:
    width = 960
    height = 1000
    fps = 60
    bg = (26, 35, 126)
    dark = (0, 0, 81)
    white = (255, 255, 255)
    red = (244, 67, 54)
    red_200 = (239, 154, 154)
    green = (0, 255, 0)
    blue = (33, 150, 243)

    move_area = 0.02
    speed = 50
    
    
    @classmethod
    def set_default_window_position(cls):
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (cls.width,0)

