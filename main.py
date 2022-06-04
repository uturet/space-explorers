import pygame
import os
import math
import random


WIDTH = 960
HEIGHT = 1080
FPS = 60
BLACK = (0, 0, 0)
DARK = (0, 0, 81)
WHITE = (255, 255, 255)
RED = (244, 67, 54)
RED_200 = (239, 154, 154)
GREEN = (0, 255, 0)
BLUE = (33, 150, 243)
choose_pos = (WIDTH/2, HEIGHT/2)
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (WIDTH,0)


class Player(pygame.sprite.Sprite):
    radius = 100
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.image = pygame.Surface((50, 50))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
    
    def update(self):
        self.rect.x += 5
        if self.rect.left > WIDTH:
            self.rect.right = 0
    
    def show_area(self):
        pygame.draw.circle(screen, BLUE, self.pos, self.radius, 1)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
for i in range(10):
    all_sprites.add(Player((random.randint(0, WIDTH), random.randint(0, HEIGHT))))

def draw_sprites_areas(sprites):
    for sp in sprites:
        sp.show_area()


def is_mouse_intersect_sprites(sprites):
    for sp in sprites:
        if math.hypot(choose_pos[0] - sp.pos[0]) < sp.radius and \
            math.hypot(choose_pos[1] - sp.pos[1]) < sp.radius:
            return True
    return False
         


running = True
while running:
    screen.fill(BLACK)
    
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.MOUSEMOTION:
            choose_pos = event.pos
            
    draw_sprites_areas(all_sprites)
    if is_mouse_intersect_sprites(all_sprites):
        pygame.draw.circle(screen, RED, choose_pos, 100, 1)
    else:
        pygame.draw.circle(screen, RED_200, choose_pos, 100, 1)


    
    all_sprites.draw(screen)
    clock.tick(FPS)
    pygame.display.flip()

pygame.quit()
            
        