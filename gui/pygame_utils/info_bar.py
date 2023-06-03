import pygame

class InfoBar :
    def __init__(self, pathRepoBar:str, pos:tuple[int,int], currentAmount:int=10, fullAmount:int=10) :
        self.fullAmount = fullAmount

        n = self.get_n(currentAmount)

        self.path_to_bar = pathRepoBar
        self.img = pygame.image.load(f"{pathRepoBar}/{n}.png").convert()
        self.rect = self.img.get_rect(topleft = pos)
    
    def get_n (self, amount) :
        return max(0, min(round((amount//self.fullAmount) * 10, -1), self.fullAmount))
    
    def update (self, hero) :
        """ Attention : Il faudrat blit après sinon le changement ne sera pas affiché """
        self.fullAmount = hero._hpMax
        self.img = pygame.image.load(f"{self.path_to_bar}/{self.get_n(hero._hp)}.png").convert()