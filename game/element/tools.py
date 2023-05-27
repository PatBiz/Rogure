#******************************* Importations : ********************************

# Modules persos :
import game._game as Gme
from .creature import Hero
from .decor import FixedElement
from .equipment import Item


#******************************** Fonctions : **********************************

def meet (a, b) :
    if type(a) == type(b) :
        return False

    if isinstance(b, FixedElement) :
        if isinstance(a, Hero) :
            b.action()
        return False

    if isinstance(b, Item) :
        if isinstance(a, Hero) : # and inventory not full
            b.getTaken()
            return True
        Gme.theGame()._floor.cacheItem(b)
        return True

    a.hit(b)
    return b.isDead()