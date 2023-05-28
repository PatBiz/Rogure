#******************************* Importations : ********************************

# Built-in modules :
from typing import Optional

# Modules persos :
import game._game as Gme
from .elem import Element


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
        raise NotImplementedError


class Stairs (FixedElement) :
    def __init__ (self , name: Optional[str] = 'Stairs') :
        FixedElement.__init__(self, name, 'E')

    @staticmethod
    def action () :
        G = Gme.theGame() #Optimise le code en réduisant le nmbre d'appel
        G._level += 1
        G.buildFloor()
        G.addMessage(f"The {G._hero._name} goes down")


class Chest (FixedElement) :
    def __init__ (self , name: Optional[str] = 'Chest') :
        FixedElement.__init__(self, name, 'm')

    @staticmethod
    def action () :
        G = Gme.theGame() #Optimise le code en réduisant le nmbre d'appel
        ... #Je le laisse pour Paul 