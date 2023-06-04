import pygame
from functools import partial

from pygame_utils import Button, Trigger
from button_actions import start_rogure, load_rogure, quit_rogure

import env_var as ev


def mainMenuInit (screen) :

    """ Initialise le contenu de la fenêtre de démarrage ET actualise la liste des boutons. """

    # Création des composants de la fenêtre :

    TitleImage = pygame.image.load("gui/assets/title.png").convert_alpha()
    BgTitleImage = pygame.image.load("gui/assets/background/mainMenu_Background.jpg").convert()

    startButton= Button(path="gui/assets/Buttons/main_menu/start_button.png",
                        pos=(545,250),
                        action=partial(start_rogure, screen))
    loadButton = Button(path="gui/assets/Buttons/main_menu/load_button.png",
                        pos=(550,345),
                        action=partial(load_rogure, screen))
    quitButton = Button(path="gui/assets/Buttons/main_menu/quit_button.png",
                        pos=(555,440),
                        action=quit_rogure)

    # Insertion des composants sur la fenêtre :

    screen.blit(BgTitleImage, (0,0))
    screen.blit(TitleImage, (400,20))
    screen.blit(startButton.img, startButton.rect)
    screen.blit(loadButton.img, loadButton.rect)
    screen.blit(quitButton.img, quitButton.rect)
    pygame.display.flip()


    ev.__dict__["listButtons"] = [startButton, loadButton, quitButton]
    ev.__dict__["status"] = Trigger.InMainMenu