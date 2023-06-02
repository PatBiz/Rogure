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
    equipments = {0: [ Elmt.Equipment("potion","!",usage=Elmt.heal), Elmt.Gold("gold","o") ],
                  1: [ Elmt.equipment.Wearable("sword","weapon",("strength",3)), Elmt.Equipment("bow"), Elmt.Equipment("potion","!",usage=lambda hero : Elmt.teleport(hero , unique = True)), Elmt.Gold("gold","o",3) ],
                  2: [ Elmt.equipment.Wearable("chainmail","armor",("defense",3)), Elmt.Gold("gold","o",5) ],
                  3: [ Elmt.Equipment("portoloin","w",usage=lambda hero : Elmt.teleport(hero , unique = False)), Elmt.Gold("gold","o",7) ]
    }
    monsters = {0: [ Elmt.Monster("Goblin",4), Elmt.Monster("Bat",2,"W") ],
                1: [ Elmt.Monster("Ork",6,strength=2), Elmt.Monster("Blob",10) ],
                5: [ Elmt.Monster("Dragon",20,strength=3) ]
    }
    actions = {
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

    __slot__ = ("buildFloor", "addMessage", "readMessages", "randElement", "randEquipment", "randMonster", "select", "update_floor_affichage", "play")

    def __init__(self , hero:Optional[Elmt.Hero]=None , floor_level:int=1 , floor:Optional[Flr.Map]=None) :
        self._hero = hero or Elmt.Hero()
        self._floor = floor
        self._floor_level = floor_level
        self._message = []

    def __getattr__(self, __name: str) :
        if __name in {"__hero__", "_hero"} :
            return self._hero
        if __name in {"__floor__", "_floor"} :
            return self._floor
        if __name in {"__floor_level__", "_floor_level"} :
            return self._floor_level
        if __name in {"__message__", "_message"} :
            return self._message

        return self.__dict__[__name]

    def __setattr__(self, __name:str, __value) :
        if __name in {"__hero__", "_hero"} :
            self.__dict__["_hero"] = __value
        if __name in {"__floor__", "_floor"} :
            self.__dict__["_floor"] = __value
        if __name in {"__floor_level__", "_floor_level"} :
            self.__dict__["_floor_level"] = __value
        if __name in {"__message__", "_message"} :
            self.__dict__["_message"] = __value
        
        self.__dict__[__name] = __value

    def buildFloor (self) :
        m = self._floor = Flr.Map(hero = self._hero)
        m.put_Elmt_At_Coord(Elmt.Stairs(), m._rooms[-2].center())

    def addMessage(self , msg:str) :
        self._message.append(msg)

    def readMessages(self):
        if self._message:
            s = "".join(f"{msg}. " for msg in self._message)
            self._message = []
            return s
        return ""

    def randElement (self , collection) :
        X = rd.expovariate(1/self._floor_level)
        for rarity in collection :
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
    
    def update_floor_affichage (self, nuageDeVisibilite=True) :
        self._floor.uncacheAllItem()
        if nuageDeVisibilite :
            print(self._floor)
            print(self._floor.nuageVisibilite())
            return self._floor.nuageVisibilite()
        print(self._floor)
        return repr(self._floor)
    
    def update_effects(self):
        Hstatut = self._hero._statut
        eff=0
        while eff<len(Hstatut):
            apply=Flr.room.TrapRoom.trapTypes[Hstatut[eff][0]][0]
            apply(self._hero,Hstatut[eff][1])
            Hstatut[eff][2]-=1
            if not Hstatut[eff][2]:
                Hstatut.pop(eff)
            else:
                eff+=1

    def play(self):
        """Main game loop"""
        self.buildFloor()
        print("--- Welcome Hero! ---")
        
        while self._hero._hp > 0:
            print()
            print (f"--- Etage {self._floor_level} ---")
            self.update_floor_affichage(nuageDeVisibilite=True)
            print(self._hero.description())
            print(self.readMessages())

            c = getch()
            if c!="i":
                self.update_effects() 
            if c in _Game.actions:
                _Game.actions[c](self._hero)
            self._floor.moveAllMonsters()
        
        print("--- Game Over ---")


#********************************* Singleton : *********************************

def theGame(game = _Game()):
    return game