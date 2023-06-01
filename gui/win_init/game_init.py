import pygame
from functools import partial


from pygame_utils import Button
from button_actions import open_inventory, equip#, close_inventory

from game import theGame


def gameInit (screen) :

    """ Initialise la fenêtre de jeu ET renvoie la liste des boutons. """ 

    # Création des composants de la fenêtre :

    BgGameImage = pygame.image.load("gui/assets/background/inGame_Background.jpg").convert()

    backPackButton = Button(path="gui/assets/Buttons/in_game/inventory_btn.png",
                        pos=(495,250),
                        action=partial(open_inventory, screen))

    # Insertion des composants sur la fenêtre :

    screen.blit(BgGameImage, (-200,-50))
    screen.blit(backPackButton.img, backPackButton.rect)
    pygame.display.flip()

    return [backPackButton,]

def inventoryInit (screen) :
    """ Initialise l'affiche de l'inventaire du joueur ET renvoie la liste des boutons. """

    # Création des composants de la fenêtre :

    PopUpInventory = pygame.image.load("gui/assets/background/inventory_PopUp.png").convert_alpha()

    lCases = []

    screen.blit(PopUpInventory, (375,70))
    #screen.blit(inventoryButton.img, inventoryButton.rect) # ----- Qd l'inventaire sera un btn

    i = 0
    for k in range (3) :
        for x in [395,490,588,683] :
            lCases.append(Button(path="gui/assets/Buttons/in_game/inventory/inv-case_btn.png",
                    pos=(x,147+k*98),
                    action=partial(equip, screen, i)))
            screen.blit(lCases[-1].img, lCases[-1].rect)
            i += 1
   
    
    pygame.display.flip()

    return lCases + []