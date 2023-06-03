



#******************************* Importations : ********************************

# Built-in modules :
from typing import Optional

# Modules persos :
import game._game as Gme
from .item import Item


#********************************** Classes : **********************************

#-------------------------------------------------------------------------------
#                               EQUIPMENT ELEMENT
#-------------------------------------------------------------------------------

class Equipment (Item) :
    def __init__ (self , name:str , abbrv:Optional[str]=None , usage=None) :
        Item.__init__(self, name, abbrv)
        self.usage = usage

    def getUse (self , creature) :
        if self.usage :
            Gme.theGame().addMessage(msg = f"The {creature._name} uses the {self._name}")
            return self.usage(creature)

        Gme.theGame().addMessage(msg = f"The {self._name} is not usable")
        return False

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

class Wearable(Equipment):
    """A wearable equipment."""
    def __init__(self, name, place, effect, abbrv="", usage=None):
        Equipment.__init__(self, name, abbrv, usage)
        self.place = place
        self.effect = effect

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