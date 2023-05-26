#******************************* Importations : ********************************

# Built-in modules :
from typing import Optional

# Modules persos :
import game._game as Gme
from .elem import Element


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


class Equipment (Item) :
    def __init__ (self , name:str , abbrv:Optional[str]=None , usage=None) :
        Element.__init__(self, name, abbrv)
        self.usage = usage

    def getTaken (self) :
        G = Gme.theGame() #Optimise le code en réduisant le nmbre d'appel
        G.addMessage(msg = f"You pick up a {self._name}")
        G._hero.take(self)

    def use (self , creature) :
        if self.usage :
            Gme.theGame().addMessage(msg = f"The {creature._name} uses the {self._name}")
            return self.usage(creature)
        
        Gme.theGame().addMessage(msg = f"The {self._name} is not usable")
        return False

class Gold (Item) :
    ...