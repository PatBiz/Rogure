#******************************* Importations : ********************************

# Built-in modules :
import pygame

# Modules persos :
from button_actions import quit_rogure, close_inventory
from gui.pygame_utils.button import find_button_pressed
from gui.pygame_utils import getCell_In_Room
from gui.sprite_getter import getElementSprite_Path

# Variables d'environnement :
import env_var as ev


#******************************** Fonctions : **********************************

#-------------------------------------------------------------------------------
#                                 GAME LOOP
#-------------------------------------------------------------------------------


def gameLoop (screen) :

    unknownItem = "gui/assets/Items/none_item.png"
    emptyCell = "gui/assets/Decors/empty.png"

    g = ev.game
    m = g.__floor__

    " Affichages des cases visibles & des éléments dessus : "

    rVisible = m.get_VisibleZone()
    rCellInRange = getCell_In_Room(room=rVisible, lCell=ev.listMapCell)



    printer = ev.printer
    print(printer.pos)
    for coord, cell in zip(rVisible, rCellInRange) :
        if m.isVisible(coord) :
            screen.blit((img := cell.img), printer.pos)
            elem = m.get_Elmt_At_Coord(coord)
            if not isinstance(elem , str) :
                try : eSprite = getElementSprite_Path[elem._abbrv]
                except KeyError : eSprite = pygame.image.load(unknownItem).convert_alpha()
                screen.blit(eSprite, printer.pos)
        else :
            screen.blit((img := pygame.image.load(emptyCell).convert_alpha()), printer.pos)
        pygame.display.update(img.get_rect())
        if coord.x == m.size-1 :
            printer.breakLine()
        else :
            printer.move_right()
    printer.reset()
    

    for button in ev.listButtons :
        screen.blit(button.img, button.rect)
        pygame.display.update(button.rect)

    for event in pygame.event.get() :

        if event.type == pygame.QUIT : #On ferme la fenêtre + stoppe le jeu
            quit_rogure()
        
        elif event.type == pygame.MOUSEBUTTONDOWN :
            button = find_button_pressed(ev.listButtons, event.pos)
            if button :
                try : screen.blit(button.active_img, button.rect)
                except AttributeError : pass
                pygame.display.update(button.rect)
                ev.__dict__["listButtons"] = button.action()


#-------------------------------------------------------------------------------
#                               INVENTORY LOOP
#-------------------------------------------------------------------------------


def inventoryLoop (screen) :

    for button in ev.listButtons :
        screen.blit(button.img, button.rect)
    pygame.display.flip()

    mouse_pos = pygame.mouse.get_pos()
    for button in ev.listButtons :
        if button.rect.collidepoint(mouse_pos) :
            screen.blit(button.active_img, button.rect)
            pygame.display.update(button.rect)

    for event in pygame.event.get() :

        if event.type == pygame.QUIT : #On ferme la fenêtre + stoppe le jeu
            quit_rogure()

        elif event.type == pygame.MOUSEBUTTONDOWN :
            button = find_button_pressed(ev.listButtons, event.pos)
            if button :
                try : screen.blit(button.active_img, button.rect)
                except AttributeError : pass 
                pygame.display.update(button.rect)
                button.action()
            else :
                ev.__dict__["listButtons"] = close_inventory(screen)