#******************************* Importations : ********************************

# Built-in modules :
from typing import Optional

#Modules persos :
import game._game as Gme
from .elem import Element
from .equipment import Equipment

from utils import statically_typed_function


#********************************** Classes : **********************************

#-------------------------------------------------------------------------------
#                               CREATURE ELEMENT
#-------------------------------------------------------------------------------


class Creature (Element) : #Classe abstraite
    def __init__ (self, name:str, hp:int, abbrv:Optional[str]=None, strength:Optional[int]=1) :
        Element.__init__(self, name, abbrv)
        self._hp = hp
        self._strength = strength

    def description(self):
        raise NotImplementedError

    def takeDamage (self, n) :
        self._hp -= n

    def hit (self, other):
        Gme.theGame().addMessage(msg = f"The {other._name} hits the {self.description()}")
        other.takeDamage(self._strength)

    def isDead (self) :
        return self._hp <= 0


class Monster (Creature) :
    def __init__ (self, name:str, hp:int, abbrv:Optional[str]=None, strength:Optional[int]=1) :
        Creature.__init__(self, name, hp, abbrv, strength)

    def description(self):
        return f'<{self._name}>({self._hp})'


class Hero (Creature) :
    def __init__ (self,
                  name: Optional[str] = 'Hero',
                  hp: Optional[int] = 10,
                  abbrv: Optional[str] = '@',
                  strength: Optional[int] = 2,
                  inventory: Optional[list] = None) :
        Creature.__init__(self, name, hp, abbrv, strength)
        self._inventory = inventory or []

    def description (self) :
        return f'<{self._name}>({self._hp}){self._inventory}'

    def fullDescription (self) :
        s = ""
        for attr , attrValue in self.__dict__.items() :
            if attr == '_inventory' :
                continue
            s += f"> {attr[1:] if attr[0]=='_' else attr} : {attrValue}\n"
        s += f"> INVENTORY : {[i._name for i in self.__dict__['_inventory']]}"
        return s

    @statically_typed_function
    def take (self, item:Equipment) :
        self._inventory.append(item)

    @statically_typed_function
    def use (self, item:Equipment) :
        if item not in self._inventory :
            raise ValueError(f"<{self.name}> doesn't have <{item.name}>")
        if item.use(self) :
            self._inventory.remove(item)