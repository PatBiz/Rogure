#******************************* Importations : ********************************

# Built-in modules :
from typing import Optional
from copy import copy
import random as rd

# Modules persos :
import game._game as Gme
from .elem import Element
from .equipment import StackOfItems



#********************************** Classes : **********************************

#-------------------------------------------------------------------------------
#                                FIXED ELEMENT
#-------------------------------------------------------------------------------


class FixedElement (Element) : #Classe abstraite
    """ Représente l'ensemble des objets fixes ET irrécupérable sur la Map """
    def __init__ (self, name:str, abbrv:str) :
        Element.__init__(self, name, abbrv)

    @staticmethod
    def action () :
        raise NotImplementedError("FixedElement is an abstract class.")


class Stairs (FixedElement) :
    def __init__ (self , name: Optional[str] = 'Stairs') :
        FixedElement.__init__(self, name, 'E')

    @staticmethod
    def action () :
        G = Gme.theGame() #Optimise le code en réduisant le nmbre d'appel
        G.__floor_level__ += 1
        G.buildFloor()
        G.addMessage(f"The {G.__hero__._name} goes down")


class Chest (FixedElement) :
    def __init__ (self , name: Optional[str] = 'Chest') :
        FixedElement.__init__(self, name, 'm')

    @staticmethod
    def action () :
        G = Gme.theGame()
        for _ in range(3) :
            G.__hero__.take(G.randElement(G.chestContent))


class Shop(FixedElement):
    def __init__(self, name="Shop", abbrv="$"):
        FixedElement.__init__(self, name, abbrv)
        self.items={}

    def stock(self):
        pass

    def action(self):
        G = Gme.theGame() #Optimise le code en réduisant le nmbre d'appel
        G.addMessage(f"The {G.__hero__._name} opens the shop")
        self.purchase()

    def purchase(self):
        pass
        
