#******************************* Importations : ********************************

# Built-in modules :
import pygame

# Modules persos :
from button_actions import start_rogure,quit_rogure, open_inventory, close_inventory
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

    # Récupération des variables d'environnements :
    g = ev.game
    m = g.__floor__

    #Affichage des cellules visible et des éléments à l'intérieur :
    visibleZone = m.get_VisibleZone()
    cellInVisibleZone = getCell_In_Room(room=visibleZone, lCell=ev.listMapCell)

    printer = ev.printer
    for lc in cellInVisibleZone :
        for cell in lc :
            printer.print_image(screen, cell.img)
            elem = m.get_Elmt_At_Coord(cell.coord_in_map)
            if not isinstance(elem, str) : #Si il y a un élément dans cette cellule
                try : eSprite = getElementSprite_Path[elem._abbrv]
                except KeyError : eSprite = pygame.image.load(ev.unknownItem).convert_alpha()
                screen.blit(eSprite, printer.pos)
            printer.move_right()
        printer.breakLine()
    printer.reset()
    pygame.display.flip()

    #Actualisation des informations sur le héro :
    BgInfoHero = pygame.image.load("gui/assets/background/hero_info_wide.png").convert_alpha()
    #Bar de Pv
    #Bar de mana
    #Bar de satiété
    #Porte-monnaie
    #Lvl
    #Effet
    pygame.display.update(BgInfoHero.get_rect())

    """"print (f"--- Etage {self._floor_level} ---")"""

    #Reset des boutons :
    for button in ev.listButtons :
        screen.blit(button.img, button.rect)
        pygame.display.update(button.rect)

    mouse_pos = pygame.mouse.get_pos()
    for button in ev.listButtons :
        if button.rect.collidepoint(mouse_pos) :
            screen.blit(button.active_img, button.rect)
            pygame.display.update(button.rect)

    #Gestion des events :
    for event in pygame.event.get() :

        if event.type == pygame.QUIT : #On ferme la fenêtre + stoppe le jeu
            quit_rogure()

        # SIMULATION de Game.play()
        elif event.type == pygame.KEYDOWN :
            try : 
                ev.game_actions[event.key](g.__hero__)
                print(f"{event.key} has been pressed")
                print(g.__floor__.pos(g.__hero__))
            except KeyError :
                match event.key :
                    case pygame.K_i : 
                        ev.__dict__["listButtons"] = open_inventory(screen)
                    case pygame.K_m :
                        ev.__dict__["generateMap"] = True
                        ev.__dict__["listButtons"] = start_rogure(screen)
                    case _ : pass

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