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

    emptyCell = "gui/assets/Decors/empty.png"

    """ Initialise la fenêtre de jeu ET renvoie la liste des boutons. """ 

    # Chargement du jeu :

    g = ev.game
    g.buildFloor() #¤#
    m = g.__floor__

    # Création des cases de la map :

    printer = ev.printer
    l = []
    lCell = []
    for coord in m.getIterator_coord() :
        char = m.get_Elmt_At_Coord(coord)
        match char :
            case ' ' :
                print(f"{char} ==> Empty case")
                l.append( MapCell(printer.get_image(emptyCell), coord) )
            case '#' :
                print(f"{char} ==> Wall case")
                l.append( MapCell(printer.get_image(getWallSprite_Path(m, coord)), coord) )
            case _ :
                print(f"{char} ==> Floor case")
                l.append( MapCell(printer.get_image(getFloorSprite_Path()), coord) )
        if coord.x == m.size-1 :
            printer.breakLine()
            lCell.append( l )
            l = []
        else :
            printer.move_right()
    printer.reset()
    pygame.display.flip()

    # Création des composants secondaires de la fenêtre en jeu :

    BgGameImage = pygame.image.load("gui/assets/background/inGame_Background.jpg").convert()

    InfoHero = pygame.image.load("gui/assets/background/hero_info.png").convert_alpha()

    backPackButton = Button(path="gui/assets/Buttons/in_game/inventory_btn.png",
                        pos=(495,250),
                        action=partial(ba.open_inventory, screen))

    screen.blit(BgGameImage, (-200,-50))
    screen.blit(InfoHero, (0,0))
    screen.blit(backPackButton.img, backPackButton.rect)
    pygame.display.flip()

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