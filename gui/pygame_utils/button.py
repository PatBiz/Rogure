import pygame


class Button :
    def __init__ (self, path, action, pos:tuple[int,int]=(0,0), alpha:bool=True) :
        if alpha :
            self.img = pygame.image.load(path).convert_alpha()
            try :
                n = len(path.split('.')[-1]) + 1
                self.active_img = pygame.image.load(path[:-n]+"_active"+path[-n:]).convert_alpha()
            except FileNotFoundError : self.active_img = self.img
        else :
            self.img = pygame.image.load(path).convert()
            try :
                n = len(path.split('.')[-1]) + 1
                self.active_img = pygame.image.load(path[:-n]+"_active"+path[-n:]).convert()
            except FileNotFoundError : self.active_img = self.img

        self.rect = self.img.get_rect(topleft = pos)

        self.action = action


def find_button_pressed (listButton:list[Button] , event_pos) :
    for button in listButton :
        if button.rect.collidepoint(event_pos) :
            return button