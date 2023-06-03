import pygame

class InfoBar :
    def __init__(self, pathRepoBar:str, pos:tuple[int,int], look:str, currentAmount:int=10, fullAmount:int=10) :
        self.fullAmount = fullAmount
        self.look = look

        n = self.get_n(currentAmount)

        self.path_to_bar = pathRepoBar
        self.img = pygame.image.load(f"{pathRepoBar}/{n}.png").convert()
        self.rect = self.img.get_rect(topleft = pos)

    def get_n (self, amount) :
        return int(max(0, min(round((amount/self.fullAmount) * 10, 0), self.fullAmount)))

    def update (self, hero) :
        """ Attention : Il faudrat blit après sinon le changement ne sera pas affiché """
        self.fullAmount = hero.__dict__[f"{self.look}Max"]
        self.img = pygame.image.load(f"{self.path_to_bar}/{self.get_n(hero.__dict__[self.look])}.png").convert()