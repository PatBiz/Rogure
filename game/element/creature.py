#******************************* Importations : ********************************

# Built-in modules :
from typing import Optional

#Modules persos :
import game._game as Gme
from .elem import Element
from .equipment import Equipment, Wearable
from .item import Item, StackOfItems, Gold

from utils import statically_typed_function


#********************************** Classes : **********************************

#-------------------------------------------------------------------------------
#                               CREATURE ELEMENT
#-------------------------------------------------------------------------------


class Creature (Element) : #Classe abstraite
    def __init__ (self, name:str, hp:int, abbrv:Optional[str]=None, visible=True, strength:Optional[int]=1, speed:Optional[int]=1) :
        Element.__init__(self, name, abbrv, visible)
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
        if isinstance(self,Monster) and self.capacity:
            self.useCapacity(other)

    def isDead (self) :
        return self._hp <= 0


class Monster (Creature) :
    def __init__ (self, name:str, hp:int, abbrv:Optional[str]=None, visible=True, strength:Optional[int]=1, speed:Optional[int]=1, xpAmount=0, loot=None, capacity=None) :
        Creature.__init__(self, name, hp, abbrv, visible, strength, speed)
        self.xpAmount = int(hp*strength/2) if not xpAmount else xpAmount
        self.loot = loot
        self.capacity = capacity

    def description(self):
        return f'<{self._name}>({self._hp})'
    
    def dropLoot(self):
        if self.loot!=None:
            Gme.theGame()._hero.take(self.loot)

    def useCapacity(self, creature):
        if self.capacity:
            if self._name == "Invisible":
                return self.capacity(self)
            return self.capacity(creature)


class Hero (Creature) :
    def __init__ (self,
                  name: Optional[str] = 'Hero',
                  hp: Optional[int] = 10,
                  abbrv: Optional[str] = '@',
                  visible=True,
                  strength: Optional[int] = 2,
                  defense = 3,
                  inventory: Optional[list] = None,
                  porte_monnaie: Optional[int]=0,
                  level: Optional[int]=0,
                  xp = 0,
                  seuilXp=10,
                  hpMax = None) :
        Creature.__init__(self, name, hp, abbrv, visible, strength, speed=1)
        self._hpMax = hpMax or hp
        self._defense = defense
        self._inventory = inventory or []
        self._porte_monnaie = porte_monnaie
        self._level = level
        self.xp = xp
        self.seuilXp = seuilXp
        self._statut=[]
        self.weapon = None
        self.armor = [None,None]

    def description (self) :
        return f'<{self._name}>({self._hp}/{self._hpMax})|{self._level}|xp: {self.xp}/{self.seuilXp}{"{"+str(self._porte_monnaie)+"}"}{self._inventory}'

    def fullDescription (self) :
        s = ""
        for attr , attrValue in self.__dict__.items() :
            if attr not in ['_inventory', '_statut'] :
                s += f"> {attr[1:] if attr[0]=='_' else attr} : {attrValue}\n"
        s += f"> STATUT : {[eff for eff in self._statut]}\n"
        s += f"> INVENTORY : {[i._name for i in self.__dict__['_inventory']]}\n"
        return s

    def inventoryIsFull (self) :
        return len(self._inventory)>12

    @statically_typed_function
    def take (self, item:Item) :
        if isinstance(item, Gold) :
            self._porte_monnaie += item._amount
        else:
            self._inventory.append(item)    
            if self.inventoryIsFull() : #¤Max Inventory Length¤#
                self.drop(item)

    @statically_typed_function
    def use (self, item:Item) :
        if item not in self._inventory :
            raise ValueError(f"<{self._name}> doesn't have <{item._name}>")
        if isinstance(item,Wearable):
            self.wear(item)
            self._inventory.remove(item)
        elif item.getUse(self) :
            self._inventory.remove(item)

    @statically_typed_function
    def drop (self, item:Item) :
        if item not in self._inventory :
            raise ValueError(f"<{self._name}> doesn't have <{item._name}>")

        G = Gme.theGame()
        m = G.__floor__
        posHero = m.get_Pos_Of_Elmt(self)

        cachedItem = m.get_cachedItem_At_Coord(posHero)
        if cachedItem :
            if isinstance(cachedItem, StackOfItems) :
                cachedItem.append(item)
                item = cachedItem
            else :
                item = StackOfItems(content=[cachedItem, item])

        self._inventory.remove(item)
        m.cacheItem_At_Coord(item, posHero)
        G.addMessage(f"{self._name} drops {item._name}")

    def hpPourcent(self):
        return self._hp*100//self._hpMax
    
    def levelUp(self):
        self.xp-=self.seuilXp
        self.seuilXp*=2
        self._level+=1
        self._hpMax += 3
        self._hp = self._hpMax
        if not self._level%2 and self._level>1:
            self._strength += 1

    def wear(self, equipment):
        if equipment.place=="weapon":
            if self.weapon!=None:
                self.unwear("weapon",None)
            self.weapon = equipment
        elif equipment.place=="helmet":
            if self.armor[0]!=None:
                self.unwear("armor",0)
            self.armor[0] = equipment
        else:
            if self.armor[1]!=None:
                self.unwear("armor",1)
            self.armor[1] = equipment
        equipment.applyEffect(self)

    def unwear(self,place,index):
        if place=="weapon":
            if self.weapon!=None:
                equipment = self.weapon
                self.take(self.weapon)
                self.weapon = None
        if place=="armor":
            if self.armor[index]!=None:
                equipment = self.armor[index]
                self.take(self.armor[index])
                self.armor[index] = None
        equipment.removeEffect(self)