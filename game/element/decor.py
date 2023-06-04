#******************************* Importations : ********************************

# Built-in modules :
import random as rd

# Modules persos :
import game._game as Gme
from .elem import Element
from .item import StackOfItems, Key
from utils.keyboard_listener import getch

# Modules pour l'interface graphique :
from gui.pygame_utils.triggers import Trigger

# Variables d'environnement (pour l'interface graphique) :
import env_var as ev #c'est normal si sur VsCode c'est souligné


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
    def get_sprite() :
        return "gui/assets/Decors/stairs.png"

    @staticmethod
    def action () :
        G = Gme.theGame() #Optimise le code en réduisant le nmbre d'appel
        G.__floor_level__ += 1
        G.buildFloor()
        ev.__dict__["generateMap"] = True
        G.addMessage(f"The {G.__hero__._name} goes down")


class Chest (FixedElement) :
    def __init__ (self) :
        FixedElement.__init__(self, 'Chest', 'm')

    @staticmethod
    def get_sprite() :
        return "gui/assets/Decors/chest_close.png"

    @staticmethod
    def action () :
        G = Gme.theGame()
        for i,item in enumerate (G.__hero__._inventory) :
            if isinstance(item, Key) :
                G.__hero__._inventory.pop(i)
                StackOfItems(content=[G.randElement(G.equipments,2) for _ in range(3)]).getTaken()
                #Je peux le faire car il y a qu'un seul chest sur la map
                m = G.__floor__
                for e,coord in m._elem.items() :
                    if isinstance(e, Chest) :
                        m.rm(coord)
                        m.put(coord, OpenedChest())
                        return True
        G.addMessage("A key is necessary")


class OpenedChest (FixedElement) : #J'en ai besoin sinon ce sera plus dur pour moi de mettre un coffre ouvert sur la map.
    def __init__(self) :
        FixedElement.__init__(self, 'OpenedChest', 'n')

    @staticmethod
    def get_sprite () :
        return "gui/assets/Decors/chest_open.png"

    @staticmethod
    def action () :
        Gme.theGame().addMessage("This chest has already been opened")


class Seller (FixedElement) :
    def __init__(self):
        FixedElement.__init__(self, "Shop", "$")
        self.items = self.stock()

    @staticmethod
    def get_sprite ():
        return f"gui/assets/Characters/Allies/Seller_{rd.choice(['l','r'])}.png"

    def stock (self) :
        G = Gme.theGame()
        objects = [G.equipments[0][0],G.equipments[1][1],G.equipments[1][2]]
        stock = [[obj,3,3] for obj in objects]
        return stock

    def action (self) :
        G = Gme.theGame() #Optimise le code en réduisant le nmbre d'appel
        G.addMessage(f"The {G.__hero__._name} opens the shop")
        ev.__dict__["status"] = Trigger.InShop
        self.purchase()

    def purchase(self):
        G = Gme.theGame() #Optimise le code en réduisant le nmbre d'appel
        purchase = True
        while purchase:
            interface = ''
            for obj in range(len(self.items)):
                interface += f"\t- ({obj}) <{self.items[obj][0]}>, price: {self.items[obj][1]} golds, stock: {self.items[obj][2]}\n"
            G.addMessage("Do you want to buy something?>\n"+interface+"Your golds: "+str(G.__floor__._hero._porte_monnaie))
            print(G.readMessages())
            choice = getch()
            if not choice in ['0','1','2']:
                return False
            if G.__floor__._hero._porte_monnaie<self.items[int(choice)][1]:
                G.addMessage("You try to scam me?")
                return False
            G.__floor__._hero.take(self.items[int(choice)][0])
            self.items[int(choice)][2]-=1
            G.__floor__._hero._porte_monnaie -= self.items[int(choice)][1]
            G.addMessage("Thanks. Do you want to buy something else? (y/n)\n"+"Your golds: "+str(G.__floor__._hero._porte_monnaie))
            print(G.readMessages())
            if getch()!='y':
                purchase = False
        G.addMessage("Goodbye")
