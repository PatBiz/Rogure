#******************************* Importations : ********************************

# Built-in modules :
from typing import Optional
from copy import copy
import random as rd

# Modules persos :
from floor import Coord
import element as Elmt
import floor as Flr

from utils import getch


#********************************** Classes : **********************************

#-------------------------------------------------------------------------------
#                                    GAME
#-------------------------------------------------------------------------------


class _Game() :
    equipments = {0: [ Elmt.Equipment("potion","!",usage=Elmt.heal), Elmt.Equipment("gold","o") ],
                  1: [ Elmt.Equipment("sword"), Elmt.Equipment("bow"), Elmt.Equipment("potion","!",usage=lambda hero : Elmt.teleport(hero , unique = True)) ],
                  2: [ Elmt.Equipment("chainmail") ],
                  3: [ Elmt.Equipment("portoloin","w",usage=lambda hero : Elmt.teleport(hero , unique = False)) ]
    }
    monsters = {0: [ Elmt.Monster("Goblin",4), Elmt.Monster("Bat",2,"W") ],
                1: [ Elmt.Monster("Ork",6,strength=2), Elmt.Monster("Blob",10) ],
                5: [ Elmt.Monster("Dragon",20,strength=3) ]
    }
    _actions = {
        # Actions de déplacement :
        'z' : lambda hero : theGame()._floor.moveHero(hero , Coord(0,-1))   ,
        's' : lambda hero : theGame()._floor.moveHero(hero , Coord(0,1))    ,
        'd' : lambda hero : theGame()._floor.moveHero(hero , Coord(1,0))    ,
        'q' : lambda hero : theGame()._floor.moveHero(hero , Coord(-1,0))   ,
        ' ' : lambda hero : theGame()._floor.moveHero(hero , Coord(0,0))    ,
        # Actions sur l'inventaire :
        'u' : lambda hero : hero.use(_Game.select(hero._inventory))         ,
        'h' : lambda hero : hero.drop(_Game.select(hero._inventory))        ,
        # Autre actions :
        'i' : lambda hero : theGame().addMessage(hero.fullDescription())    ,
        'k' : lambda hero : hero.__setattr__('_hp' , 0)
    }

    def __init__(self , hero:Optional[Elmt.Hero]=None , level:int=1 , floor:Optional[Flr.Map]=None) :
        self._hero = hero or Elmt.Hero()
        self._level = level
        self._floor = floor
        self._message = []
        

    def buildFloor (self) :
         m = self._floor = Flr.Map(hero = self._hero)
         m.put_Elmt_At_Coord(Elmt.Stairs() , m._rooms[-1].center())

    def addMessage(self , msg:str) :
        self._message.append(msg)

    def readMessages(self):
        if self._message:
            s = "".join(f"{msg}. " for msg in self._message)
            self._message = []
            return s
        return ""

    def randElement (self , collection) :
        X = rd.expovariate(1/self._level)
        for rarity in collection.keys() :
            if rarity > X : break
            rarityMax = rarity
        return copy(rd.choice(collection[rarityMax]))

    def randEquipment (self) :
        return self.randElement(_Game.equipments)

    def randMonster (self) :
        return self.randElement(_Game.monsters)
    
    @staticmethod
    def select(l) :
        print(f"Choose item> {[f'{i}: {item._name}' for i,item in enumerate(l)]}")
        while True :
            try :
                return l[int(getch())]
            except (IndexError , ValueError) :
                return None

    def play(self):
        """Main game loop"""
        self.buildFloor()
        print("--- Welcome Hero! ---")
        while self._hero._hp > 0:
            self._floor.uncacheAllItem()
            print()
            print(self._floor)
            print(self._hero.description())
            print(self.readMessages())
            c = getch()
            if c in _Game._actions:
                _Game._actions[c](self._hero)
            self._floor.moveAllMonsters()
        print("--- Game Over ---")


#********************************* Singleton : *********************************

def theGame(game = _Game()):
    return game