import pygame
from options import Options


class Field(pygame.sprite.Sprite):
    def __init__(self):
        self.dimens = (4000, 4000)
        self.pos = [0, 0]
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(self.dimens)
        self.image.fill(Options.dark)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        
    def move_left(self):
        self.pos[0] = min(self.dimens[0]/2, self.pos[0] + Options.speed)
        self.rect.center = self.pos
        
    def move_right(self):
        self.pos[0] = max(Options.width-self.dimens[0]/2, self.pos[0] - Options.speed)
        self.rect.center = self.pos
        
    def move_top(self):
        self.pos[1] = min(self.dimens[1]/2, self.pos[1] + Options.speed) 
        self.rect.center = self.pos
        
    def move_bot(self):
        self.pos[1] = max(Options.height-self.dimens[1]/2, self.pos[1] - Options.speed)
        self.rect.center = self.pos