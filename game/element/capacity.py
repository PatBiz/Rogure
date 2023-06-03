#******************************* Importations : ********************************

# Built-in modules :
import random as rd

#Module perso :
import game._game as Gme
from .creature import Creature
from .creature import Hero


#******************************** Fonctions : **********************************

def heal (creature:Creature):
    if isinstance(creature,Hero):
        creature._hp = creature._hpMax if creature._hp + 3>creature._hpMax else creature._hp + 3
        return True

def teleport(creature:Creature, unique:bool) :
    m = Gme.theGame().__floor__
    r = rd.choice(m._rooms)
    m[creature] = m.randEmptyCoordInRoom(r)
    return unique

def becomeVisible(element):
    if not element.visible:
        element._abbrv = element._name[0]
        element.visible = True
