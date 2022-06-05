import random
from player import Player


def seed_players_rand(count, state):
    for i in range(count):
        state.bggroup.add(Player((
            random.randint(0, state.bg.dimens[0]),
            random.randint(0, state.bg.dimens[1])
        ), state.bg.image))


def fill_players(size, state):
    for y in range(state.bg.image.get_height()//size):
        for x in range(state.bg.image.get_width()//size):
            p = Player((x*size, y*size), state.bg.image)
            state.bggroup.add(p)
