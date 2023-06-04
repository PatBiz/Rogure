import pygame
import random as rd

from game.floor import Coord

# Wall :
def getWallSprite(m, cwall):
    try :
        bcase = m.get_Elmt_At_Coord(cwall+Coord(0,1))
        if not isinstance(bcase, str) :
            bcase = '.'
    except IndexError : bcase = ' '

    if bcase == '.' :
        imgPath = rd.choice(["gui/assets/Decors/walls/horizontal/horizontal_wall_1.png",
                          "gui/assets/Decors/walls/horizontal/horizontal_wall_2.png",
                          "gui/assets/Decors/walls/horizontal/horizontal_wall_3.png"])
    elif bcase == ' ' :
        try :
            b2case = m.get_Elmt_At_Coord(cwall+Coord(0,2))
            if not isinstance(b2case, str) :
                b2case = '.'
        except IndexError : b2case = ' '
        if b2case != '#' :
            imgPath = rd.choice(["gui/assets/Decors/walls/horizontal/horizontal_wall_1.png",
                          "gui/assets/Decors/walls/horizontal/horizontal_wall_2.png",
                          "gui/assets/Decors/walls/horizontal/horizontal_wall_3.png"])
    try :
        return pygame.image.load(imgPath).convert()
    except UnboundLocalError :
        imgPath = "gui/assets/Decors/walls/vco_wall.png"
        return pygame.image.load(imgPath).convert()

# Floor :
def getFloorSprite () :
    imgPath = rd.choice(["gui/assets/Decors/floors/floor_1.png",
                      "gui/assets/Decors/floors/floor_2.png",
                      "gui/assets/Decors/floors/floor_3.png",
                      "gui/assets/Decors/floors/floor_4.png"])

    return pygame.image.load(imgPath).convert()

# Cloud :
def getCloudSprite () :
    return pygame.image.load("gui/assets/Decors/clouds/cloud_3.png").convert_alpha()

# Element :
def getElementSprite (elem) :
    return pygame.image.load(elem.get_sprite()).convert_alpha()
    #raise KeyError("Pour l'instant y a rien")