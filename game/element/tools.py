#******************************* Importations : ********************************

# Modules persos :
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
        if isinstance(a, Hero) :
            b.getTaken()
            return True
        return False

    a.hit(b)
    return b.isDead()