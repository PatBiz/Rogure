import pygame
from copy import copy

class Printer :
    def __init__ (self, pos:tuple, lmove:int) :
        self.pos = pos
        self.lmove = lmove
        self.posDepart = copy(pos)

    def reset (self) :
        self.pos = copy(self.posDepart)
   
    def breakLine (self) :
        self.pos = (self.posDepart[0], self.pos[1]+self.lmove)
    
    def move_right (self) :
        self.pos = (self.pos[0]+self.lmove, self.pos[1])

    def get_image (self, path, alpha:bool=True) :
        if alpha :
            return pygame.image.load(path).convert_alpha()
        return pygame.image.load(path).convert()
    
    def print_image (self, screen, img) :
        screen.blit(img, self.pos)
        pygame.display.update(img.get_rect())
    
    def printµget_image(self, screen, path, alpha:bool=True) :
        img =  self.get_image(path, alpha)
        self.print_image(screen, img)
        return img
    
    def get_rect (self) :
        return tuple(*self.pos,80,80)