#******************************* Importations : ********************************

# Built-in modules :
import random as rd

#Module perso :
import game._game as Gme
from .creature import Creature


#******************************** Fonctions : **********************************

def heal (creature:Creature):
    creature._hp += 3
    return True

def teleport(creature:Creature, unique:bool) :
    m = Gme.theGame()._floor
    r = rd.choice(m._rooms)
    m[creature] = m.randEmptyCoordInRoom(r)
    return unique