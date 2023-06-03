#******************************* Importations : ********************************

# Built-in modules :
from typing import Optional

# Modules persos :
import game._game as Gme
from .elem import Element
from floor.room import TrapRoom
import floor as Flr

from utils import statically_typed_function


#********************************** Classes : **********************************

#-------------------------------------------------------------------------------
#                                 ITEM ELEMENT
#-------------------------------------------------------------------------------


class Item (Element) : #Classe abstraite
    def __init__ (self, name, abbrv) :
        Element.__init__(self, name, abbrv)

    def description(self) :
        return f"<{self._name}>"

    def getTaken (self) :
        G = Gme.theGame() #Optimise le code en réduisant le nombre d'appel
        G.addMessage(msg = f"You pick up a {self._name}")
        G.__hero__.take(self)


class StackOfItems (Item) :
    def __init__ (self, name="Stack", content=Optional[list[Item]]) :
        Item.__init__(self, name, abbrv="¤")
        self._content = content or []

    def extend (self, other) :
        self._content.extend(other._content)

    @statically_typed_function
    def append (self, item:Item) :
        if isinstance(item, StackOfItems) :
            self.extend(item)
        self._content.append(item)
    
    def pop (self, indice=-1) :
        return self._content.pop(indice)

    def getTaken (self) :
        G = Gme.theGame() #Optimise le code en réduisant le nombre d'appel
        s = ""
        for item in self._content :
            G.__hero__.take(item)
            s += f" a {item._name},"
        G.addMessage(msg = f"You pick up{s[:-1]}")


class Gold (Item) :
    def __init__ (self , name:str , abbrv:Optional[str]=None , amount=1) :
        Item.__init__(self, name, abbrv)
        self._amount = amount

    def getTaken (self) :
        G = Gme.theGame() #Optimise le code en réduisant le nombre d'appel
        G.addMessage(msg = f"You pick up {self._amount} coin(s)")
        G.__hero__.take(self)


class Trap(Item) :
    def __init__(self, name="Trap", abbrv="_", effect=None, power=0):
        Item.__init__(self,name, Flr.Map.ground if abbrv=="_" else abbrv)
        self.effect=effect
        self.power=power
        self.actived=True

    def getTaken(self):
        if self.actived :
            G = Gme.theGame() #Optimise le code en réduisant le nmbre d'appel
            G._hero._statut.append([self.effect,self.power,TrapRoom.trapTypes[self.effect][1]])      #Effet, puissance, temps(en tours)
            G.addMessage(f"The {G._hero._name} is {self.effect}")
            self.actived=False
            return True


class Key (Item) :
    def __init__ (self) :
        Item.__init__(self, "Key", "µ")