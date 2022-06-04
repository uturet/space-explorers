import random
from player import Player


def seed_players(count, players_sprites, field):
    for i in range(count):
        players_sprites.add(Player((
            random.randint(0, field.dimens[0]),
            random.randint(0, field.dimens[1])
        )))
