import pygame
from copy import copy

class Printer :
    def __init__ (self, pos:tuple, lmove:int) :
        self.pos = pos
        self.lmove = lmove
        self.posDepart = copy(pos)

    def reset (self) :
        self.pos = copy(self.posDepart)
    
    def goDown (self) :
        self.pos = (self.pos[0], self.pos[1]+self.lmove)
    
    def breakLine (self) :
        self.pos = (self.posDepart[0], self.pos[1]+self.lmove)
    
    def move_right (self) :
        self.pos = (self.pos[0]+self.lmove, self.pos[1])
    
    def print_image (self, path, alpha:bool=True) :
        if alpha :
            img = pygame.image.load(path).convert_alpha()
        else :
            img = pygame.image.load(path).convert()