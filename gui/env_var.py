from __future__ import annotations
import pygame

from gui.pygame_utils import Printer
from game import theGame
from floor import Map


"------------------------------"
" Constantes d'environnement : "
"------------------------------"


game    = theGame()
game_actions = {
        # Actions de déplacement :
        pygame.K_z : lambda hero : game.__floor__.moveHero(hero , Map.dir['z'])   ,
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
#Je ne les définis pas maintenant car le screen n'a pas encore été créé ==> pygame.error
emptyCell   : pygame.Surface
unknownItem : pygame.Surface

mapRect = pygame.Rect((246,-80), (960,960))


"-----------------------------"
" Variables d'environnement : "
"-----------------------------"


status       : str
listButtons  : list[Button]

#Permet de gérer l'affichage de la map :
listMapCell  : list[MapCell]
generateMap  : bool
updateScreen : bool

#Permet de gérer l'affichage des infos du héro :
listInfoBar : list[InfoBar]
updateInfo  : bool

def f() : print(globals())