



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

class Usable (Item) :
    def __init__ (self , name:str , abbrv:Optional[str]=None , visible=True, usage=None) :
        Item.__init__(self, name, abbrv, visible)
        self.usage = usage

    def getUse (self , creature) :
        raise NotImplementedError("Equipment is an abstract class.")
        

class Consumables(Usable):
    def __init__(self, name: str, abbrv: str | None = None, visible=True, usage=None):
        super().__init__(name, abbrv, visible, usage)

    def getUse(self, creature):
        if self.usage :
            Gme.theGame().addMessage(msg = f"The {creature._name} uses the {self._name}")
            return self.usage(creature)

        Gme.theGame().addMessage(msg = f"The {self._name} is not usable")
        return False
    
    def get_sprite (self) :
        return f"gui/assets/Items/Consumables/{self._name}.png"

class ProjectileWeapon(Usable):
    def __init__(self, name: str, abbrv: str | None = None, visible=True, usage=None):
        super().__init__(name, abbrv, visible, usage)

    def getUse(self, creature):
        if self.usage:
            Gme.theGame().addMessage(msg = f"The {creature._name} uses the {self._name}")
            Gme.theGame().addMessage("Choose a direction> z:↑, s:↓, q:←, d:→")
            print(Gme.theGame().readMessages())
            ch = getch()
            if ch not in ['z', 's', 'q', 'd']:
                return False
            dir = [Flr.Coord(0,-1),Flr.Coord(0,1),Flr.Coord(-1,0),Flr.Coord(1,0)][['z','s','q','d'].index(ch)]
            return self.usage(creature,dir)

        Gme.theGame().addMessage(msg = f"The {self._name} is not usable")
        return False


class Wearable(Usable):
    """A wearable equipment."""
    def __init__(self, name, place, effect, abbrv="", visible=True, usage=True):
        Usable.__init__(self, name, abbrv, visible, usage)
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

    def get_sprite (self) :
        return f"gui/assets/Items/Equipments/Shield/{self._name}.png"


class Bow(ProjectileWeapon):
    def __init__(self, name: str, abbrv: str | None = None, visible=True, usage=None):
        super().__init__(name, abbrv, visible, usage)

    def get_sprite (self) :
        return f"gui/assets/Items/Equipments/Shield/{self._name}.png"


class Wand(ProjectileWeapon):
    def __init__(self, name: str, abbrv: str | None = None, visible=True, usage=None):
        super().__init__(name, abbrv, visible, usage)

    def get_sprite (self) :
        return f"gui/assets/Items/Equipments/Shield/{self._name}.png"


class Armor(Wearable):
    def __init__(self, name, place, effect, abbrv="", visible=True, usage=True):
        super().__init__(name, place, effect, abbrv, visible, usage)

    def get_sprite (self) :
        return f"gui/assets/Items/Equipments/Shield/{self._name}.png"


class Shield(Wearable):
    def __init__(self, name, place, effect, abbrv="", visible=True, usage=True):
        super().__init__(name, "weapon", effect, abbrv, visible, usage)

    def get_sprite (self) :
        return f"gui/assets/Items/Equipments/Shield/{self._name}.png"