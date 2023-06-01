import pygame
import random as rd

from gui.button_actions import quit_rogure, close_inventory
from pygame_utils import find_button_pressed , Button, Printer
import gui.gui_mainloop as gui_ml

from game.floor import Coord

#----------
# GAME LOOP
#----------


def getWallSprite_Img (m, cwall) :
    
    try : rcase = m.get_Elmt_At_Coord(cwall+Coord(0,1))
    except IndexError : rcase = None
    try : lcase = m.get_Elmt_At_Coord(cwall+Coord(0,-1))
    except IndexError : lcase = None
    
    try : b1case = m.get_Elmt_At_Coord(cwall+Coord(1,0))
    except IndexError : b1case = None
    try : b2case = m.get_Elmt_At_Coord(cwall+Coord(-1,0))
    except IndexError : b2case = None

    "gui/assets/Decors/walls/.../....png"


    " --- Cas mur plein -- "

    if rcase == lcase == b1case == b2case == '#' :
        return  "gui/assets/Decors/walls/full_wall.png"

    " --- Cas mur simple --- "

    #Horizontal
    if rcase == lcase == '#' :
        return rd.choice(["gui/assets/Decors/walls/horizontal/horizontal_wall_1.png",
                          "gui/assets/Decors/walls/horizontal/horizontal_wall_2.png",
                          "gui/assets/Decors/walls/horizontal/horizontal_wall_3.png"])
    #Vertical
    if b1case == b2case == '#' : #Pour l'instant y en a qu'un mais ce serait bien d'en avoir 3 comme en haut
        return rd.choice(["gui/assets/Decors/walls/horizontal/vertical_wall_1.png"])
    
    " --- Cas mur en coins --- "

    #Haut droit OU gauche
    if b1case == '#' : #Coins haut
        #Coins haut droit
        if rcase  == '#' : 
            return "gui/assets/Decors/walls/corner/corner_b2r.png"
        #Coins haut gauche
        return "gui/assets/Decors/walls/corner/corner_b2l.png"
    
    #Bas droit OU gauche
    if b2case == '#' : #Coins haut
        #Coins bas droit
        if rcase  == '#' : 
            return "gui/assets/Decors/walls/corner/corner_b1r.png"
        #Coins bas gache
        return "gui/assets/Decors/walls/corner/corner_b1l.png"
    
    raise NotImplementedError (f"""
?{b1case}?
{lcase}%{rcase}
?{b2case}?
                               """)


def getFloorSprite () :

def getElementSprite (abbrv) :



def inGameLoop (screen) :

    " Chargement du jeu : "

    g = gui_ml.game

    " Affichage de la map : "

    m = g.__floor__
    m_repr = g.update_floor_affichage()

    printer = Printer(pos=(0,0), lmove=lCase)

    # Plaçage des murs

    for char,coord in zip(m_repr, m.getIterator_coord()) :
        match char :
            case ' ' :
                continue
            case '\n' :
                printer.breakLine()
            case '#' :
                printer.print_image(getWallSprite(m, coord))
            case '.' :
                printer.print_image(getFloorSprite(m))
            case _ :
                printer.print_image(getFloorSprite(m))
                printer.print_image(getElementSprite(m))
        printer.move_right()
    
    for event in pygame.event.get() :

        if event.type == pygame.QUIT : #On ferme la fenêtre + stoppe le jeu
            quit_rogure()
        
        elif event.type == pygame.MOUSEBUTTONDOWN :
            button = find_button_pressed(gui_ml.list_Buttons, event.pos)
            if button :
                try : screen.blit(button.active_img, button.rect)
                except AttributeError : pass 
                pygame.display.update(button.rect)
                gui_ml.status, gui_ml.list_Buttons = button.action()


#------------------
#       INVENTORY
#------------


def inInventoryLoop (screen) :

    for button in gui_ml.list_Buttons :
        screen.blit(button.img, button.rect)
    pygame.display.flip()

    mouse_pos = pygame.mouse.get_pos()
    for button in gui_ml.list_Buttons :
        if button.rect.collidepoint(mouse_pos) :
            screen.blit(button.active_img, button.rect)
            pygame.display.update(button.rect)

    for event in pygame.event.get() :

        if event.type == pygame.QUIT : #On ferme la fenêtre + stoppe le jeu
            quit_rogure()

        elif event.type == pygame.MOUSEBUTTONDOWN :
            button = find_button_pressed(gui_ml.list_Buttons, event.pos)
            if button :
                try : screen.blit(button.active_img, button.rect)
                except AttributeError : pass 
                pygame.display.update(button.rect)
                button.action()
            else :
                gui_ml.status, gui_ml.list_Buttons = close_inventory(screen)
