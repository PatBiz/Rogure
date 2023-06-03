#******************************* Importations : ********************************

# Built-in modules :
...

# Modules persos :
import game._game as Gme
from .elem import Element
from .equipment import Equipment
from .item import StackOfItems



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
    def __init__ (self) :
        FixedElement.__init__(self, 'Stairs', 'E')

    @staticmethod
    def action () :
        G = Gme.theGame() #Optimise le code en réduisant le nmbre d'appel
        G.__floor_level__ += 1
        G.buildFloor()
        G.addMessage(f"The {G.__hero__._name} goes down")


class Chest (FixedElement) :
    def __init__ (self) :
        FixedElement.__init__(self, 'Chest', 'm')

    @staticmethod
    def action () :
        G = Gme.theGame()
        for i,item in enumerate (G.__hero__._inventory) :
            if isinstance(item, Key) :
                G.__hero__._inventory.pop(i)
                StackOfItems(content=[G.randElement(G.equipments) for _ in range(3)]).getTaken()
                #Je peux le faire car il y a qu'un seul chest sur la map
                m = G.__floor__
                for e,coord in m._elem.items() :
                    if isinstance(e, Chest) :
                        m.rm(coord)
                        m.put(OpenedChest())
            else:
                G.addMessage("A key is necessary")


class OpenedChest (FixedElement) : #J'en ai besoin sinon ce sera plus dur pour moi de mettre un coffre ouvert sur la map.
    def __init__(self) :
        FixedElement.__init__(self, 'OpenedChest', 'n')

    @staticmethod
    def action () :
        Gme.theGame().addMessage("This chest has already been opened")


class Seller (FixedElement) :
    def __init__(self):
        FixedElement.__init__(self, "Shop", "$")
        self.items = {}

    def stock (self) :
        pass

    def action (self) :
        G = Gme.theGame() #Optimise le code en réduisant le nmbre d'appel
        G.addMessage(f"The {G.__hero__._name} opens the shop")
        self.purchase()

    def purchase(self):
        pass