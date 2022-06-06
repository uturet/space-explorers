import random
from game_objects.player import Player
import pygame
from core.config import Config


def seed_players_rand(count, state):
    for i in range(count):
        state.bggroup.add(Player((
            random.randint(0, state.bg.dimens[0]),
            random.randint(0, state.bg.dimens[1])
        ), state.bg.image))


def seed_players_rand_static(count, sprite):
    for i in range(count):
        image = pygame.Surface((10, 10))
        image.fill(Config.red)
        pos = (
            random.randint(0, sprite.rect.width),
            random.randint(0, sprite.rect.height)
        )
        sprite.image.blit(image, pos)


def fill_players(size, state):
    for y in range(state.bg.image.get_height()//size):
        for x in range(state.bg.image.get_width()//size):
            p = Player((x*size, y*size), state.bg.image)
            state.bggroup.add(p)
