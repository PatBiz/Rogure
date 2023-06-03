#******************************* Importations : ********************************

# Built-in modules :
import pygame
import time

# Modules persos :
from gui.pygame_utils import find_button_pressed, getCell_In_Room
from gui.sprite_getter import getElementSprite, getCloudSprite
from gui.button_actions import start_rogure,quit_rogure, open_inventory, close_inventory

# Variables d'environnement :
import env_var as ev


#******************************** Fonctions : **********************************

#-------------------------------------------------------------------------------
#                                 GAME LOOP
#-------------------------------------------------------------------------------

def _update_screen(screen):
    # Récupération des variables d'environnements :
    g = ev.game
    m = g.__floor__

    #Affichage des cellules visible et des éléments à l'intérieur :
    visibleZone = m.get_VisibleZone()
    cellInVisibleZone = getCell_In_Room(room=visibleZone, lCell=ev.listMapCell)
    rNuageVisible = getCell_In_Room(room=visibleZone, lCell=m.nuageVisibilite(6).split('\n'))

    printer = ev.printer
    for lc, ln in zip(cellInVisibleZone, rNuageVisible) :
        for cell, cloudCell in zip(lc, ln) :
            printer.print_image(screen, cell.img)
            if cloudCell == " ":
                printer.print_image(screen, getCloudSprite())
            else:
                elem = m.get_Elmt_At_Coord(cell.coord_in_map)
                if not isinstance(elem, str) : #Si il y a un élément dans cette cellule
                    try : eSprite = getElementSprite(elem)
                    except FileNotFoundError : eSprite = ev.unknownItem
                    print(elem._name)
                    screen.blit(eSprite, printer.pos)
            #pygame.display.update(cell.img.get_rect(topleft=printer.pos))
            printer.move_right()
        printer.breakLine()
    printer.reset()

    pygame.display.update(ev.mapRect)

    #pygame.display.flip()

    #pygame.event.pump()

def _update_info_hero (screen) :
    # Récupération des variables d'environnements :
    g = ev.game

    #Actualisation des informations sur le héro :
    for infobar in ev.listInfoBar :
        infobar.update(g.__hero__)
        screen.blit(infobar.img, infobar.rect)
        pygame.display.update(infobar.rect)
    # TODO :
    #BgInfoHero = pygame.image.load("gui/assets/background/hero_info_wide.png").convert_alpha()
    #Bar de pv
    #Bar de mana
    #Bar de satiété
    #Porte-monnaie
    #Lvl
    #Effet


def gameLoop (screen) :

    if ev.updateScreen :
        _update_screen(screen)
        """
        while screen.get_at((768, 433)) == (16, 22, 22, 255) :
            #ev.f()
            start_rogure(screen)
            time.sleep(0.03)
        """
        ev.__dict__["updateScreen"] = False
    
    if ev.updateInfo :
        _update_info_hero(screen)
        ev.__dict__["updateScreen"] = False
    

    """"print (f"--- Etage {self._floor_level} ---")"""

    #Reset des boutons :
    for button in ev.listButtons :
        screen.blit(button.img, button.rect)
        pygame.display.update(button.rect)
    
    #pygame.event.pump()

    mouse_pos = pygame.mouse.get_pos()
    for button in ev.listButtons :
        if button.rect.collidepoint(mouse_pos) :
            screen.blit(button.active_img, button.rect)
            pygame.display.update(button.rect)

    #pygame.event.pump()

    #Gestion des events :
    g = ev.game
    for event in pygame.event.get() :

        if event.type == pygame.QUIT : #On ferme la fenêtre + stoppe le jeu
            quit_rogure()

        # SIMULATION de Game.play()
        elif event.type == pygame.KEYDOWN :
            try : 
                ev.game_actions[event.key](g.__hero__)
                print(f"{event.key} has been pressed")
                print(g.__floor__.pos(g.__hero__))
                g.__floor__.moveAllMonsters()
                g.update_effects()
                ev.__dict__["updateScreen"] = True
                ev.__dict__["updateInfo"] = True
            except KeyError :
                match event.key :
                    case pygame.K_i :
                        ev.__dict__["listButtons"] = open_inventory(screen)
                    case pygame.K_m :
                        ev.__dict__["generateMap"] = True
                        ev.__dict__["listButtons"] = start_rogure(screen)
                    case _ : pass

        elif event.type == pygame.MOUSEBUTTONDOWN :
            print(f"{event.pos} --> {screen.get_at((event.pos))}") #¤DEBUG¤#
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