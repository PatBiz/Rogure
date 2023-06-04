#******************************* Importations : ********************************

# Built-in modules :
import pygame


#******************************** Fonctions : **********************************

def deathScreenInit (screen) :

    """ Initialise le contenu de la fenêtre de Game Over ET actualise la liste des boutons. """

    # Création des composants de la fenêtre :

    BgGameOverImage = pygame.image.load("gui/assets/background/gameOver_Background.jpg").convert()

    # Insertion des composants sur la fenêtre :

    screen.blit(BgGameOverImage, (0,0))
    pygame.display.flip()