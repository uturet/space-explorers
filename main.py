import pygame
import math
import random

from pyparsing import Opt
from Field import Field
from Player import Player
from options import Options

Options.set_default_window_position()  

class Mouse:
    pos = (Options.width/2, Options.height/2)

    @property
    def pos_x(self):
        x = round(mouse.pos[0] - (field.pos[0] - (field.dimens[0]/2)))
        return max(0, min(x, field.dimens[0]))
    
    @property
    def pos_y(self):
        y = round(mouse.pos[1] - (field.pos[1] - (field.dimens[1]/2)))
        return max(0, min(y, field.dimens[1]))

mouse = Mouse()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((Options.width, Options.height))
field = Field()

players_sprites = pygame.sprite.Group()
interface_sprites = pygame.sprite.Group()
interface_sprites.add(field)

def seed_players(count):
    for i in range(count):
        players_sprites.add(Player((
            random.randint(0, field.dimens[0]), 
            random.randint(0, field.dimens[1])
        )))
seed_players(200)

def get_mouse_intersect_sprites(sprites):
    int_sprites = set()
    for sp in sprites:
        if math.hypot(mouse.pos_x - sp.pos[0], mouse.pos_y - sp.pos[1]) < sp.radius:
            int_sprites.add(sp)
    return int_sprites


class EventHandler():
    
    def mousemotion_handler(self, event):
        if event.type == pygame.MOUSEMOTION:
            mouse.pos = event.pos
            
            move_field = set()
            if Options.width*Options.move_area > event.pos[0]:
                move_field.add(field.move_left)
            if (Options.width - Options.width*Options.move_area) < event.pos[0]:
                move_field.add(field.move_right)
            if Options.height*Options.move_area > event.pos[1]:
                move_field.add(field.move_top)
            if (Options.height - Options.height*Options.move_area) < event.pos[1]:
                move_field.add(field.move_bot)
    
    def mousebuttondown_handler(self, event, new_items):
        if event.type == pygame.MOUSEBUTTONDOWN:
            new_items.add(Player)

class Game(EventHandler):
    
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("My Game")

    def main_loop(self):
        move_field = set()
        new_items = set()
        running = True
        
        while running:
            screen.fill(Options.bg)
            interface_sprites.draw(screen)
            
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                self.mousemotion_handler(event)
                self.mousebuttondown_handler(event, new_items)
                
            for move in move_field:
                move()
                    
            for sp in players_sprites:
                sp.show_area(field)
            
            int_sprites = get_mouse_intersect_sprites(players_sprites)
            if int_sprites:
                pygame.draw.circle(screen, Options.red, mouse.pos, 100, 2)
            else:
                pygame.draw.circle(screen, Options.white, mouse.pos, 100, 2)

            if new_items:
                if int_sprites:
                    color = Options.red
                else:
                    color = Options.white
                for i in new_items:
                    players_sprites.add(i((mouse.pos_x, mouse.pos_y), color))
                new_items = set()
            
            players_sprites.draw(field.image)
            clock.tick(Options.fps)
            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    g = Game()
    g.main_loop()
