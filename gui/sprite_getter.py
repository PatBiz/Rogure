import random as rd

from game.floor import Coord

def getWallSprite_Path(m, cwall):
    try :
        bcase = m.get_Elmt_At_Coord(cwall+Coord(0,1))
        if not isinstance(bcase, str) :
            bcase = '.'
    except IndexError : bcase = ' '

    if bcase in {'.', ' '}:
        return rd.choice(["gui/assets/Decors/walls/horizontal/horizontal_wall_1.png",
                          "gui/assets/Decors/walls/horizontal/horizontal_wall_2.png",
                          "gui/assets/Decors/walls/horizontal/horizontal_wall_3.png"])
    return "gui/assets/Decors/walls/vco_wall.png"
    

def getFloorSprite_Path () :
    return rd.choice(["gui/assets/Decors/floors/floor_1.png",
                      "gui/assets/Decors/floors/floor_2.png",
                      "gui/assets/Decors/floors/floor_3.png",
                      "gui/assets/Decors/floors/floor_4.png"])

getElementSprite_Path = {

}