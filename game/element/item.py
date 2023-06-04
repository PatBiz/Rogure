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
    def __init__ (self, name, abbrv, visible=True) :
        Element.__init__(self, name, abbrv, visible)

    def description(self) :
        return f"<{self._name}>"

    def getTaken (self) :
        G = Gme.theGame() #Optimise le code en réduisant le nombre d'appel
        G.addMessage(msg = f"You pick up a {self._name}")
        G.__hero__.take(self)


class StackOfItems (Item) :
    def __init__ (self, name="Stack", visible=True, content=Optional[list[Item]]) :
        Item.__init__(self, name, visible, abbrv="¤")
        self._content = content or []

    def get_sprite (self) -> str :
        n = len(self._content)
        if n<4 :
            return "gui/assets/Items/stacks/stack_stage_1.png"
        if n<7 :
            return "gui/assets/Items/stacks/stack_stage_2.png"
        return "gui/assets/Items/stacks/stack_stage_3.png"

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
    def __init__ (self , name:str , abbrv:Optional[str]=None, visible=True, amount=1) :
        Item.__init__(self, name, abbrv, visible)
        self._amount = amount

    @staticmethod
    def get_sprite () -> str :
        return "gui/assets/Items/coin.png"

    def getTaken (self) :
        G = Gme.theGame() #Optimise le code en réduisant le nombre d'appel
        G.addMessage(msg = f"You pick up {self._amount} coin(s)")
        G.__hero__.take(self)


class Effect:
    def __init__(self, type, power, rounds):
        self.type = type
        self.power = power
        self.rounds = rounds

    def __eq__(self, other):
        return self.type==other.type

    def __repr__(self) :
        return f'[{self.type}, {self.power} dmg, {self.rounds} rounds]'

    def applyEffect(self, creature):
        G = Gme.theGame() #Optimise le code en réduisant le nmbre d'appel
        for eff in range(len(creature._statut)):
            if creature._statut[eff]==self:
                creature._statut[eff].rounds = self.rounds
                G.addMessage(f"The {creature._name} is {self.type}")
                return True
        creature._statut.append(self)
        G.addMessage(f"The {creature._name} is {self.type}")
        return True

class Trap(Item) :
    def __init__(self, name="Trap", abbrv=None, visible=False, effect=None):
        Item.__init__(self,name, abbrv, visible)
        self.effect = effect
        self.actived = True

    def getTaken(self):
        if self.actived :
            if self.effect:
                self.effect.applyEffect(Gme.theGame()._hero)
                self.actived=False


class Key (Item) :
    def __init__ (self) :
        Item.__init__(self, "Key", "µ")
    
    @staticmethod
    def get_sprite () -> str :
        return "gui/assets/Items/key.png"