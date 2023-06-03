import pygame

from gui.pygame_utils import Printer

from game import theGame
#import game.floor as  
from floor import Map

" Constantes d'environnement : "

game    = theGame()
game_actions2 = theGame().actions
game_actions = {
        # Actions de déplacement :
        pygame.K_z : lambda hero : theGame().__floor__.moveHero(hero , Map.dir['z'])   ,
        pygame.K_s : lambda hero : theGame().__floor__.moveHero(hero , Map.dir['s'])   ,
        pygame.K_d : lambda hero : theGame().__floor__.moveHero(hero , Map.dir['d'])   ,
        pygame.K_q : lambda hero : theGame().__floor__.moveHero(hero , Map.dir['q'])   ,
        pygame.K_SPACE : lambda hero : theGame().__floor__.moveHero(hero , Map.dir['q']),
        # Actions sur l'inventaire :
        pygame.K_u : lambda hero : hero.use(theGame().select(hero._inventory))        ,
        pygame.K_h : lambda hero : hero.drop(theGame().select(hero._inventory))       ,
        # Autre actions :
        pygame.K_k : lambda hero : hero.__setattr__('_hp' , 0)
        #'i' : lambda hero : theGame().addMessage(hero.fullDescription())    ,
    }


printer = Printer(pos=(246,-80), lmove=80)

#Sprites courants :
emptyCell = "gui/assets/Decors/empty.png"
unknownItem = "gui/assets/Items/none_item.png"

" Variables d'environnement : "

status       : str
generateMap  : bool
listButtons  : list
listMapCell  : list