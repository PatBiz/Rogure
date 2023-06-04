#******************************* Importations : ********************************

# Built-in modules :
import pygame
from functools import partial

# Modules persos :
from gui.pygame_utils import Button, Trigger, MapCell, InfoBar
from gui.sprite_getter import getFloorSprite, getWallSprite
import button_actions as ba

# Variables d'environnement :
import env_var as ev


#******************************** Fonctions : **********************************

def deathScreenInit (screen) :

    """ Initialise le contenu de la fenêtre de Game Over ET actualise la liste des boutons. """

    # Création des composants de la fenêtre :

    BgGameOverImage = pygame.image.load("gui/assets/background/gameOver_Background.jpg").convert()

    restartButton= Button(path="gui/assets/Buttons/game_over/yes.png",
                        pos=(540,443),
                        action=partial(ba.start_rogure, screen))
    menuButton = Button(path="gui/assets/Buttons/game_over/no.png",
                        pos=(663,443),
                        action=partial(ba.back_to_menu, screen))

    # Insertion des composants sur la fenêtre :

    screen.blit(BgGameOverImage, (0,0))
    screen.blit(restartButton.img, restartButton.rect)
    screen.blit(menuButton.img, menuButton.rect)
    pygame.display.flip()

    ev.__dict__["listButtons"] = [restartButton, menuButton]
    ev.__dict__["status"] = Trigger.InMainMenu