#******************************* Importations : ********************************

# Modules persos :
import game._game as Gme
from .creature import Hero
from .decor import FixedElement
from .equipment import Item
from .equipment import Trap


#******************************** Fonctions : **********************************

def meet (a, b) :
    if type(a) == type(b) :
        return False

    if isinstance(b, FixedElement) :
        if isinstance(a, Hero) :
            b.action()
        return False

    if isinstance(b, Item) :
        if isinstance(a, Hero) :
            if isinstance(b,Trap):
                b.action()
            else:
                b.getTaken()
            return True
        Gme.theGame()._floor.cacheItem(b)
        return True

    a.hit(b)
    if b.isDead() :
        if isinstance(a,Hero):
            a.xp += b.giveXp
            if a.xp>=a.seuilXp:
                a.xp-=a.seuilXp
                a.seuilXp*=2
                a._level+=1
        return True
    return False