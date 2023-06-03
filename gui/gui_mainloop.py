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

win_init.mainMenuInit(screen)

# Boucle Principale :

"""
Hypothèse d'implémentation dans 'main.py' :
    - mettre dans 'main.py'
    - faire comme 'gui_tester.py'
"""
ev.__dict__["generateMap"] = True
while True :
    match ev.status :
        case Trigger.InMainMenu :
            loops.mainMenuLoop(screen)
        case Trigger.InGame :
            loops.gameLoop(screen)
            ...
        case Trigger.InInventory :
            loops.inventoryLoop(screen)
        #case InLoading :
        #    ...
        #case InShop :
        #    ...
        case None :
            pygame.quit()