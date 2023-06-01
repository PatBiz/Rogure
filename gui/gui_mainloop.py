import pygame

from gui.pygame_utils.triggers import Trigger, Printer
import loops
import win_init

from game import theGame

# Initialisation de la fenêtre d'affichage du jeu :

pygame.init()

screen = pygame.display.set_mode(size=(1180,700))
icon = pygame.image.load("gui/assets/rogure_icon.png").convert()
pygame.display.set_icon(icon)
pygame.display.set_caption('Rogure')


# Boucle Principale :

"""
Hypothèse d'implémentation dans 'main.py' :
    - mettre dans 'main.py'
    - faire comme 'gui_tester.py'
"""

game = theGame()

status = Trigger.InMainMenu
list_Buttons = win_init.mainMenuInit(screen)
while True :
    match status :
        case Trigger.InMainMenu :
            loops.mainMenuLoop(screen)
        case Trigger.InGame :
            loops.inGameLoop(screen)
        case Trigger.InInventory :
            loops.inInventoryLoop(screen)
        #case InLoading :
        #    ...
        case None :
            pygame.quit()