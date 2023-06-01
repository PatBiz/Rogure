#******************************* Importations : ********************************

# Built-in modules :
from typing import Optional

# Modules persos :
import game._game as Gme
from .elem import Element

from utils import statically_typed_function

#********************************** Classes : **********************************

#-------------------------------------------------------------------------------
#                               EQUIPMENT ELEMENT
#-------------------------------------------------------------------------------


class Item (Element) : #Classe abstraite
    def __init__ (self, name, abbrv) :
        Element.__init__(self, name, abbrv)

    def description(self) :
        return f"<{self._name}>"

    def getTaken (self) :
        raise NotImplementedError


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
        for item in self :
            G.__hero__.take(item)
            s += f" a {self._name},"
        G.addMessage(msg = f"You pick up{s}")


class Equipment (Item) :
    def __init__ (self , name:str , abbrv:Optional[str]=None , usage=None) :
        Item.__init__(self, name, abbrv)
        self.usage = usage

    def getTaken (self) :
        G = Gme.theGame() #Optimise le code en réduisant le nombre d'appel
        G.addMessage(msg = f"You pick up a {self._name}")
        G.__hero__.take(self)

    def getUse (self , creature) :
        if self.usage :
            Gme.theGame().addMessage(msg = f"The {creature._name} uses the {self._name}")
            return self.usage(creature)

        Gme.theGame().addMessage(msg = f"The {self._name} is not usable")
        return False


class Gold (Item) :
    def __init__ (self , name:str , abbrv:Optional[str]=None , amount=1) :
        Item.__init__(self, name, abbrv)
        self._amount = amount

    def getTaken (self) :
        G = Gme.theGame() #Optimise le code en réduisant le nombre d'appel
        G.addMessage(msg = f"You pick up {self._amount} coin(s)")
        G._hero.take(self)