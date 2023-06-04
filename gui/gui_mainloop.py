import pygame

from pygame_utils import Trigger
import loops
import win_init
import env_var as ev


# Initialisation de la fenêtre d'affichage du jeu :

pygame.init()

screen = pygame.display.set_mode(size=(1300,700))
icon = pygame.image.load("gui/assets/rogure_icon.png").convert()
pygame.display.set_icon(icon)
pygame.display.set_caption('Rogure')

ev.__dict__["emptyCell"]   = pygame.image.load("gui/assets/Decors/empty.png").convert_alpha()
ev.__dict__["unknownItem"] = pygame.image.load("gui/assets/Items/none_item.png").convert_alpha()

# Boucle Principale :

"""
Hypothèse d'implémentation dans 'main.py' :
    - mettre dans 'main.py'
    - faire comme 'gui_tester.py'
"""

ev.__dict__["generateMap"] = True
win_init.mainMenuInit(screen)
while True :
    match ev.status :
        case Trigger.InMainMenu :
            loops.mainMenuLoop(screen)
        case Trigger.InGame :
            loops.gameLoop(screen)
            if ev.game.__hero__.isDead() :
                win_init.deathScreenInit(screen)
        case Trigger.InInventory :
            loops.inventoryLoop(screen)
        #case Trigger.InLoading :
        #    ...
        #case Trigger.InShop :
        #    ...
        #case Trigger.HasLost :
            loops.deathScreenLoop(screen)
        case None :
            pygame.quit()