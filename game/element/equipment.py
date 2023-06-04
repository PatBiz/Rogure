



#******************************* Importations : ********************************

# Built-in modules :
from typing import Optional

# Modules persos :
import game._game as Gme
from .item import Item
import floor as Flr

from utils.keyboard_listener import getch


#********************************** Classes : **********************************

#-------------------------------------------------------------------------------
#                               EQUIPMENT ELEMENT
#-------------------------------------------------------------------------------

class Equipment (Item) :
    def __init__ (self , name:str , abbrv:Optional[str]=None , visible=True, usage=None) :
        Item.__init__(self, name, abbrv, visible)
        self.usage = usage

    def getUse (self , creature) :
        raise NotImplementedError("Equipment is an abstract class.")
        

"""
Avis pour Mathieu :
    Je pense qu'il faudrait fusionner Wearable et Equipment
    afin de créer une classe abstraite qui générera les classes :
        - Weapon
        - Shield
        - Armor
        - Jewelry
        ...
    La raison pour laquelle je pense ça est que Equipment possède
    les méthodes gérons l'utilisation du héro et Wearable gère les effets
    que ça donne au héro (ex : Sword => plus de dégat).
    D'ailleur avec l'exemple donné on voit bien que les classes sont complémentaires.
"""
class Consumables(Equipment):
    def __init__(self, name: str, abbrv: str | None = None, visible=True, usage=None):
        super().__init__(name, abbrv, visible, usage)

    def getUse(self, creature):
        if self.usage :
            Gme.theGame().addMessage(msg = f"The {creature._name} uses the {self._name}")
            return self.usage(creature)

        Gme.theGame().addMessage(msg = f"The {self._name} is not usable")
        return False

class ProjectileWeapon(Equipment):
    def __init__(self, name: str, abbrv: str | None = None, visible=True, usage=None):
        super().__init__(name, abbrv, visible, usage)

    def getUse(self, creature):
        if self.usage :
            Gme.theGame().addMessage(msg = f"The {creature._name} uses the {self._name}")
            Gme.theGame().addMessage("Choose a direction> z:↑, s:↓, q:←, d:→")
            print(Gme.theGame().readMessages())
            ch = getch()
            if not ch in ['z','s','q','d']:
                return False
            dir = [Flr.Coord(0,-1),Flr.Coord(0,1),Flr.Coord(-1,0),Flr.Coord(1,0)][['z','s','q','d'].index(ch)]
            return self.usage(creature,dir)

        Gme.theGame().addMessage(msg = f"The {self._name} is not usable")
        return False

class Wearable(Equipment):
    """A wearable equipment."""
    def __init__(self, name, place, effect, abbrv="", visible=True, usage=True):
        Equipment.__init__(self, name, abbrv, visible, usage)
        self.place = place
        self.effect = effect

    def getUse(self, creature):
        if self.usage :
            Gme.theGame().addMessage(msg = f"The {creature._name} wears the {self._name}")
            return creature.wear(self)

        Gme.theGame().addMessage(msg = f"The {self._name} is not usable")
        return False

    def applyEffect(self,creature):
        if self.effect[0]=="strength":
            creature._strength += self.effect[1]
        elif self.effect[0]=="defense":
            creature._defense += self.effect[1]

    def removeEffect(self,creature):
        if self.effect[0]=="strength":
            creature._strength -= self.effect[1]
        elif self.effect[0]=="defense":
            creature._defense -= self.effect[1]

class Sword(Wearable):
    def __init__(self, name, place, effect, abbrv="", visible=True, usage=True):
        super().__init__(name, "weapon", effect, abbrv, visible, usage)

class Bow(ProjectileWeapon):
    def __init__(self, name: str, abbrv: str | None = None, visible=True, usage=None):
        super().__init__(name, abbrv, visible, usage)

class Wand(ProjectileWeapon):
    def __init__(self, name: str, abbrv: str | None = None, visible=True, usage=None):
        super().__init__(name, abbrv, visible, usage)

class Armor(Wearable):
    def __init__(self, name, place, effect, abbrv="", visible=True, usage=True):
        super().__init__(name, place, effect, abbrv, visible, usage)

class Shield(Wearable):
    def __init__(self, name, place, effect, abbrv="", visible=True, usage=True):
        super().__init__(name, "weapon", effect, abbrv, visible, usage)