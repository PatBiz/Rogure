#******************************* Importations : ********************************

# Built-in modules :
import pygame
import time

# Modules persos :
from gui.pygame_utils import find_button_pressed, getCell_In_Room
from gui.sprite_getter import getElementSprite, getCloudSprite
from gui.button_actions import start_rogure,quit_rogure, open_inventory, close_inventory, close_shop

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
    m.uncacheAllItem()

    #Affichage des cellules visible et des éléments à l'intérieur :
    visibleZone = m.get_VisibleZone()
    cellInVisibleZone = getCell_In_Room(room=visibleZone, lCell=ev.listMapCell)
    rNuageVisible = getCell_In_Room(room=visibleZone, lCell=m.nuageVisibilite(6).split('\n'))

    printer = ev.printer
    for lc, ln in zip(cellInVisibleZone, rNuageVisible) :
        for cell, cloudCell in zip(lc, ln) :
            screen.blit(cell.img, printer.pos)
            if cloudCell == " ":
                screen.blit(getCloudSprite(), printer.pos)
            else:
                elem = m.get_Elmt_At_Coord(cell.coord_in_map)
                if not isinstance(elem, str) : #Si il y a un élément dans cette cellule
                    try : eSprite = getElementSprite(elem)
                    except (FileNotFoundError, AttributeError) : eSprite = ev.unknownItem
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
    InfoHero = pygame.image.load("gui/assets/background/hero_info_wide.png").convert_alpha()
    screen.blit(InfoHero, (0,0))
    pygame.display.flip()

    # Récupération des variables d'environnements :
    hero = ev.game.__hero__

    # Actualisation des barres sur le héro :
    for infobar in ev.listInfoBar :
        infobar.update(hero)
        screen.blit(infobar.img, infobar.rect)
        pygame.display.update(infobar.rect)
    
    # Actualisation des effets du héro :
    for eff,posx in zip(hero._statut, [75, 115, 155]) :
        effImg = ev.dictStatusEffect[eff[0]]
        screen.blit(effImg, (posx,35))

    level = ev.font.render(f"{hero._level}", 1, (255,255,255))
    gold = ev.font.render(f"{hero._porte_monnaie}", 1, (255,255,255))

    screen.blit(level, (100,50))
    screen.blit(gold, (100,80))

    
    #Porte-monnaie
    #Lvl
    

def gameLoop (screen) :

    if ev.generateMap :
        start_rogure(screen)

    if ev.updateScreen :
        _update_screen(screen)
        if screen.get_at((768, 433)) == (16, 22, 22, 255) :
            import win_init
            win_init.gameInit(screen)
            time.sleep(1)
        
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
                        start_rogure(screen)
                    case _ : pass

        elif event.type == pygame.MOUSEBUTTONDOWN :
            print(f"{event.pos} --> {screen.get_at((event.pos))}") #¤DEBUG¤#
            button = find_button_pressed(ev.listButtons, event.pos)
            if button :
                try : screen.blit(button.active_img, button.rect)
                except AttributeError : pass
                pygame.display.update(button.rect)
                button.action()


#-------------------------------------------------------------------------------
#                               INVENTORY LOOP
#-------------------------------------------------------------------------------


def inventoryLoop (screen) :

    for button in ev.listButtons :
        screen.blit(button.img, button.rect)
    pygame.display.flip()

    for slot in ev.listSlots :
        screen.blit(slot.img, slot.rect)
        try : screen.blit(getElementSprite(slot.content), slot.rect)
        except AttributeError : pass
    pygame.display.flip()

    g = ev.game
    mouse_pos = pygame.mouse.get_pos()
    for button in ev.listButtons :
        if button.rect.collidepoint(mouse_pos) :
            screen.blit(button.active_img, button.rect)
            pygame.display.update(button.rect)
        try : 
            item = g.__hero__._inventory[button.invId]
            itemSprite = getElementSprite(item)
            screen.blit(itemSprite, button.rect)
        except IndexError : pass

    for event in pygame.event.get() :

        if event.type == pygame.QUIT : #On ferme la fenêtre + stoppe le jeu
            quit_rogure()

        elif event.type == pygame.MOUSEBUTTONDOWN :
            button = find_button_pressed(ev.listButtons, event.pos)
            if button :
                try : screen.blit(button.active_img, button.rect)
                except AttributeError : pass 
                pygame.display.update(button.rect)
                try : button.action()
                except IndexError: pass #l'inventaire était vide
            else :
                close_inventory(screen)
        
        elif event.type == pygame.KEYDOWN :
            if event.key == pygame.K_d :
                button = find_button_pressed(ev.listButtons, pygame.mouse.get_pos())
                if button :
                    try :
                        item = g.__hero__._inventory[button.invId]
                        g.__hero__.drop(item)
                    except IndexError : pass


#-------------------------------------------------------------------------------
#                               SHOP LOOP
#-------------------------------------------------------------------------------


def shopLoop (screen) :

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
                close_shop(screen)