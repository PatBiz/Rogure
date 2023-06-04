import pygame

import env_var as ev

#matthieu je vais très franchement arréter si tu fais chier comme ça

import pygame


class Button :
    def __init__(self, path:str, action, pos:tuple[int,int], alpha:bool=True):
        if alpha:
            self.img = pygame.image.load(path).convert_alpha()
            try:
                n = len(path.split('.')[-1]) + 1
                self.active_img = pygame.image.load(f"{path[:-n]}_active{path[-n:]}").convert_alpha()
            except FileNotFoundError : self.active_img = self.img
        else:
            self.img = pygame.image.load(path).convert()
            try:
                n = len(path.split('.')[-1]) + 1
                self.active_img = pygame.image.load(f"{path[:-n]}_active{path[-n:]}").convert()
            except FileNotFoundError : self.active_img = self.img

        self.rect = self.img.get_rect(topleft = pos)

        self.action = action


def find_button_pressed (listButton:list[Button] , event_pos) :
    for button in listButton :
        if button.rect.collidepoint(event_pos) :
            return button


class InventorySlot (Button) :
    def __init__(self, path:str, action, pos:tuple[int,int], invId:int, alpha:bool=True):
        Button.__init__(self, path, action, pos, alpha)
        self.invId = invId


class HeroSlot :
    def __init__ (self, path, pos, place) :
        self.img = pygame.image.load(path).convert_alpha()
        self.rect = self.img.get_rect(topleft = pos)
        self.place = place
        self.content = None
    
    def addItem (self, item) :
        if self.content :
            ev.game.__hero__.unwear(self.place, self.index)
            ev.game.__hero__.wear(item)
            self.content = item