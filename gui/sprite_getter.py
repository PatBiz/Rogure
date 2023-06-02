import random as rd

from game.floor import Coord

def getWallSprite_Path(m, cwall) :

    #Case à droite :
    try :
        rcase = m.get_Elmt_At_Coord(cwall+Coord(0,1))
        if not isinstance(rcase, str) :
            rcase = '.'
    except IndexError : rcase = ' '
    #Case à gauche :
    try :
        lcase = m.get_Elmt_At_Coord(cwall+Coord(0,-1))
        if not isinstance(lcase, str) :
            lcase = '.'
    except IndexError : lcase = ' '
    #Case au dessus :
    try :
        b1case = m.get_Elmt_At_Coord(cwall+Coord(1,0))
        if not isinstance(b1case, str) :
            b1case = '.'
    except IndexError : b1case = ' '
    #Case en dessous :
    try :
        b2case = m.get_Elmt_At_Coord(cwall+Coord(-1,0))
        if not isinstance(b2case, str) :
            b2case = '.'
    except IndexError : b2case = ' '


    " --- Cas mur plein --- "

    if rcase == lcase == b1case == b2case :
        return "gui/assets/Decors/walls/full_wall.png"

    " --- Cas mur simple --- "

    #Horizontal
    if {rcase, lcase} in [{'#'}, {'#','.'}, {'#',' '}] and {b1case, b2case} in [{'.'}, {' '}, {'.',' '}] :
        return rd.choice(["gui/assets/Decors/walls/horizontal/horizontal_wall_1.png",
                          "gui/assets/Decors/walls/horizontal/horizontal_wall_2.png",
                          "gui/assets/Decors/walls/horizontal/horizontal_wall_3.png"])
    #Vertical
    if {b1case, b2case} in [{'#'}, {'#','.'}, {'#',' '}] and {rcase, lcase} in [{'.'}, {' '}, {'.',' '}] :
        if rcase  == '.' :
            return "gui/assets/Decors/walls/vertical/vertical_wall_rv1.png" # fv1 == rv1 MAIS fv2 == rv2 (cas où rcase)
        if lcase == '.' :
            return "gui/assets/Decors/walls/vertical/vertical_wall_lv1.png"

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

def getFloorSprite_Path () :
    return rd.choice(["gui/assets/Decors/floors/floor_1.png",
                      "gui/assets/Decors/floors/floor_2.png",
                      "gui/assets/Decors/floors/floor_3.png",
                      "gui/assets/Decors/floors/floor_4.png"])

getElementSprite_Path = {

}