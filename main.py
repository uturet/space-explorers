import pygame
import os
import math
import random


WIDTH = 960
HEIGHT = 1000
FPS = 60
BG = (26, 35, 126)
DARK = (0, 0, 81)
WHITE = (255, 255, 255)
RED = (244, 67, 54)
RED_200 = (239, 154, 154)
GREEN = (0, 255, 0)
BLUE = (33, 150, 243)

MOVE_AREA = 0.02
SPEED = 50
move_field = set()

choose_pos = (WIDTH/2, HEIGHT/2)
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (WIDTH,0)

class Player(pygame.sprite.Sprite):
    radius = 100
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        size = 30
        rad = size/2
        self.pos = pos
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        pygame.draw.circle(self.image, BLUE, (rad, rad), rad)
        
    
    def update(self):
        self.rect.x += 5
        if self.rect.left > WIDTH:
            self.rect.right = 0
    
    def show_area(self):
        pygame.draw.circle(field.image, BLUE, self.pos, self.radius, 1)

class Field(pygame.sprite.Sprite):
    def __init__(self):
        self.dimens = (4000, 4000)
        self.pos = [0, 0]
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(self.dimens)
        self.image.fill(DARK)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        
    def move_left(self):
        self.pos[0] = min(self.dimens[0]/2, self.pos[0] + SPEED)
        self.rect.center = self.pos
        
    def move_right(self):
        self.pos[0] = max(WIDTH-self.dimens[0]/2, self.pos[0] - SPEED)
        self.rect.center = self.pos
        
    def move_top(self):
        self.pos[1] = min(self.dimens[1]/2, self.pos[1] + SPEED) 
        self.rect.center = self.pos
        
    def move_bot(self):
        self.pos[1] = max(HEIGHT-self.dimens[1]/2, self.pos[1] - SPEED)
        self.rect.center = self.pos
        
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()
players_sprites = pygame.sprite.Group()
interface_sprites = pygame.sprite.Group()
field = Field()


interface_sprites.add(field)
for i in range(200):
    players_sprites.add(Player((
        random.randint(0, field.dimens[0]), 
        random.randint(0, field.dimens[1])
    )))

def draw_sprites_areas(sprites):
    for sp in sprites:
        sp.show_area()


def is_mouse_intersect_sprites(sprites):
    x = round(choose_pos[0] - (field.pos[0] - (field.dimens[0]/2)))
    x = max(0, min(x, field.dimens[0]))
    y = round(choose_pos[1] - (field.pos[1] - (field.dimens[1]/2)))
    y = max(0, min(y, field.dimens[1]))
    
    for sp in sprites:
        if math.hypot(x - sp.pos[0], y - sp.pos[1]) < sp.radius:
            return True
    return False



running = True
while running:
    screen.fill(BG)
    interface_sprites.draw(screen)
    
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.MOUSEMOTION:
            choose_pos = event.pos
            
            move_field = set()
            if WIDTH*MOVE_AREA > event.pos[0]:
                move_field.add(field.move_left)
            if (WIDTH - WIDTH*MOVE_AREA) < event.pos[0]:
                move_field.add(field.move_right)
            if HEIGHT*MOVE_AREA > event.pos[1]:
                move_field.add(field.move_top)
            if (HEIGHT - HEIGHT*MOVE_AREA) < event.pos[1]:
                move_field.add(field.move_bot)
    
    for move in move_field:
        move()
            
            
            
    draw_sprites_areas(players_sprites)
    if is_mouse_intersect_sprites(players_sprites):
        pygame.draw.circle(screen, RED, choose_pos, 100, 2)
    else:
        pygame.draw.circle(screen, WHITE, choose_pos, 100, 2)


    
    players_sprites.draw(field.image)
    clock.tick(FPS)
    pygame.display.flip()

pygame.quit()
            
        