#******************************* Importations : ********************************

# Built-in modules :
from typing import Optional

#Modules persos :
import game._game as Gme
from .elem import Element
from .equipment import Item, StackOfItems

from utils import statically_typed_function


#********************************** Classes : **********************************

#-------------------------------------------------------------------------------
#                               CREATURE ELEMENT
#-------------------------------------------------------------------------------


class Creature (Element) : #Classe abstraite
    def __init__ (self, name:str, hp:int, abbrv:Optional[str]=None, strength:Optional[int]=1, speed:Optional[int]=1 :
        Element.__init__(self, name, abbrv)
        self._hp = hp
        self._strength = strength
        self._speed = speed

    def description(self):
        raise NotImplementedError("Creature is an abstract class.")

    def takeDamage (self, n) :
        self._hp -= n

    def hit (self, other):
        other.takeDamage(self._strength)
        Gme.theGame().addMessage(msg = f"The {self._name} hits the {other.description()}")

    def isDead (self) :
        return self._hp <= 0


class Monster (Creature) :
    def __init__ (self, name:str, hp:int, abbrv:Optional[str]=None, strength:Optional[int]=1, speed:Optional[int]=1) :
        Creature.__init__(self, name, hp, abbrv, strength, speed)

    def description(self):
        return f'<{self._name}>({self._hp})'


class Hero (Creature) :
    def __init__ (self,
                  name: Optional[str] = 'Hero',
                  hp: Optional[int] = 10,
                  abbrv: Optional[str] = '@',
                  strength: Optional[int] = 2,
                  inventory: Optional[list] = None) :
        Creature.__init__(self, name, hp, abbrv, strength, speed=1)
        self._inventory = inventory or []

    def description (self) :
        return f'<{self._name}>({self._hp}){self._inventory}'

    def fullDescription (self) :
        s = ""
        for attr , attrValue in self.__dict__.items() :
            if attr != '_inventory' :
                s += f"> {attr[1:] if attr[0]=='_' else attr} : {attrValue}\n"
        s += f"> INVENTORY : {[i._name for i in self.__dict__['_inventory']]}"
        return s

    @statically_typed_function
    def take (self, item:Item) :
        self._inventory.append(item)

    @statically_typed_function
    def use (self, item:Item) :
        if item not in self._inventory :
            raise ValueError(f"<{self.name}> doesn't have <{item.name}>")
        if item.getUse(self) :
            self._inventory.remove(item)

    @statically_typed_function
    def drop (self, item:Item) :
        if item not in self._inventory :
            raise ValueError(f"<{self.name}> doesn't have <{item.name}>")

        G = Gme.theGame()
        m = G._floor
        posHero = m.get_Pos_Of_Elmt(self)

        cachedItem = m.get_cachedItem_At_Coord(posHero)
        if m.get_cachedItem_At_Coord(posHero) :
            if isinstance(cachedItem, StackOfItems) :
                cachedItem.append(item)
                item = cachedItem
            else :
                item = StackOfItems(content=[cachedItem, item])

        self._inventory.remove(item)
        m.cacheItem_At_Coord(item, posHero)
