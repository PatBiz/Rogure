#******************************* Importations : ********************************

# Built-in modules :
import pygame
from functools import partial

# Modules persos :
from gui.pygame_utils import Button, MapCell, Trigger
from gui.sprite_getter import getFloorSprite_Path, getWallSprite_Path
import button_actions as ba

# Variables d'environnement :
import env_var as ev


#******************************** Fonctions : **********************************

#-------------------------------------------------------------------------------
#                                 GAME INIT
#-------------------------------------------------------------------------------


def gameInit (screen) :
    """ Initialise la fenêtre de jeu ET renvoie la liste des boutons. """ 
    
    # Récupération des variables d'environnements :
    g = ev.game
    g.buildFloor() #¤DEBUG¤#
    m = g.__floor__

    #Définition des cellules de la map :
    l = []
    lCell = []
    for coord in m.getIterator_coord() :
        char = m.get_Elmt_At_Coord(coord)
        match char :
            case ' ' :
                cell = MapCell(pygame.image.load(ev.emptyCell).convert_alpha() , coord)
            case '#' :
                cell = MapCell(pygame.image.load(getWallSprite_Path(m, coord)).convert_alpha() , coord)
            case _ :
                cell = MapCell(pygame.image.load(getFloorSprite_Path()).convert_alpha() , coord)
        l.append(cell)
        if coord.x == m.size-1 :
            lCell.append( l )
            l = []

    #Création des autres composants :
    BgGameImage = pygame.image.load("gui/assets/background/inGame_Background.jpg").convert()

    InfoHero = pygame.image.load("gui/assets/background/hero_info_wide.png").convert_alpha()

    backPackButton = Button(path="gui/assets/Buttons/in_game/inventory_btn.jpg",
                        pos=(155,102),
                        action=partial(ba.open_inventory, screen),
                        alpha=False)

    screen.blit(BgGameImage, (-200,-50))
    screen.blit(InfoHero, (0,0))
    screen.blit(backPackButton.img, backPackButton.rect)
    pygame.display.flip()

    # Mises à jour des variables d'environnements
    ev.__dict__["status"] = Trigger.InGame
    ev.__dict__["listMapCell"] = lCell

    return [backPackButton]


#-------------------------------------------------------------------------------
#                              INVENTORY INIT
#-------------------------------------------------------------------------------


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
                    action=partial(ba.equip, screen, i)))
            screen.blit(lCases[-1].img, lCases[-1].rect)
            i += 1
    pygame.display.flip()

    ev.__dict__["status"] = Trigger.InInventory
    
    return lCases + []