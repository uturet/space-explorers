import pygame
import math
import random
from Field import Field
from Player import Player
from options import Options

choose_pos = (Options.width/2, Options.height/2)
Options.set_default_window_position()  

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((Options.width, Options.height))
field = Field()

pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

players_sprites = pygame.sprite.Group()
interface_sprites = pygame.sprite.Group()
interface_sprites.add(field)

for i in range(200):
    players_sprites.add(Player((
        random.randint(0, field.dimens[0]), 
        random.randint(0, field.dimens[1])
    )))


def is_mouse_intersect_sprites(sprites):
    x = round(choose_pos[0] - (field.pos[0] - (field.dimens[0]/2)))
    x = max(0, min(x, field.dimens[0]))
    y = round(choose_pos[1] - (field.pos[1] - (field.dimens[1]/2)))
    y = max(0, min(y, field.dimens[1]))
    
    for sp in sprites:
        if math.hypot(x - sp.pos[0], y - sp.pos[1]) < sp.radius:
            return True
    return False


move_field = set()
running = True
while running:
    screen.fill(Options.bg)
    interface_sprites.draw(screen)
    
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.MOUSEMOTION:
            choose_pos = event.pos
            
            move_field = set()
            if Options.width*Options.move_area > event.pos[0]:
                move_field.add(field.move_left)
            if (Options.width - Options.width*Options.move_area) < event.pos[0]:
                move_field.add(field.move_right)
            if Options.height*Options.move_area > event.pos[1]:
                move_field.add(field.move_top)
            if (Options.height - Options.height*Options.move_area) < event.pos[1]:
                move_field.add(field.move_bot)
    
    for move in move_field:
        move()
            
    for sp in players_sprites:
        sp.show_area(field)
    if is_mouse_intersect_sprites(players_sprites):
        pygame.draw.circle(screen, Options.red, choose_pos, 100, 2)
    else:
        pygame.draw.circle(screen, Options.white, choose_pos, 100, 2)

    players_sprites.draw(field.image)
    clock.tick(Options.fps)
    pygame.display.flip()

pygame.quit()         
        