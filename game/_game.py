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
    def __init__(self , hero:Optional[Elmt.Hero]=None , floor_level:int=1 , floor:Optional[Flr.Map]=None) :
        self._hero = hero or Elmt.Hero()
        self._floor = floor
        self._floor_level = floor_level
        self._message = []

    # ¤¤¤¤¤¤¤¤¤¤ CLASS ATTRIBUTES ¤¤¤¤¤¤¤¤¤¤ #
    equipments = {0: [ Elmt.equipment.Consumables("potion","!",usage=Elmt.heal), Elmt.Gold("gold","o") ],
                  1: [ Elmt.equipment.Sword("sword","weapon",("strength",1)), Elmt.equipment.Consumables("potion","!",usage=lambda hero : Elmt.teleport(hero , unique = True)), Elmt.equipment.ProjectileWeapon("dague",usage=lambda hero,dir: Elmt.Creature.throw(hero,hero._strength,True,dir)),Elmt.Gold("gold","o",2) ],
                  2: [ Elmt.equipment.Shield("shield","weapon",("defense",1),abbrv="♦"), Elmt.Gold("gold","o",3), Elmt.equipment.Bow("bow",usage=lambda hero,dir: Elmt.Creature.throw(hero,3*hero._strength//2,False,dir)) ],
                  3: [ Elmt.equipment.Armor("helmet","helmet",("defense",1)), Elmt.Gold("gold","o",4) ],
                  4: [ Elmt.equipment.Armor("chainmail","chestplate",("defense",2)), Elmt.Gold("gold","o",5) ],
                  5: [ Elmt.equipment.Consumables("portoloin","w",usage=lambda hero : Elmt.teleport(hero , unique = False)), Elmt.Gold("gold","o",7) ]
    }
    effects = {"burned": (lambda creature, power : creature.takeDamage(power), 3),
                "paralized": (lambda a,b : print("Cc"), 4), 
                "poisoned": (lambda creature, power : creature.takeDamage(power), 2)
    } #Prendre tours + 1
    monsters = {0: [ Elmt.Monster("Goblin",6,strength=2), Elmt.Monster("Bat",4,"W") ],
                1: [ Elmt.Monster("Wolf",6,'L',strength=3,speed=2), Elmt.creature.DistanceMonster("Archers",5,strength=3,xpAmount=8) ],
                2: [ Elmt.Monster("Spider",6,capacity = lambda hero : Elmt.item.Effect("poisoned",2,_Game.effects["poisoned"][1]).applyEffect(hero)), Elmt.Monster("Invisible", 8, strength=4,visible=False,capacity=lambda self: Elmt.capacity.becomeVisible(self)) ],
                4: [ Elmt.Monster("Ork",12,strength=6), Elmt.Monster("Blob",15,strength=5) ],
                8: [ Elmt.Monster("Dragon",30,strength=10) ]
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

    # ¤¤¤¤¤¤¤¤¤¤¤¤¤¤ DUNDERS ¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤ #
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

    def randElement (self , collection, upgrade=0) :
        X = rd.expovariate(5/(self._floor_level + upgrade))
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
            #print(self._floor)
            print(self._floor.nuageVisibilite())
            return self._floor.nuageVisibilite()
        #print(self._floor)
        return repr(self._floor)
    
    def update_effects(self):
        Hstatut = self._hero._statut
        eff=0
        while eff<len(Hstatut):
            apply=_Game.effects[Hstatut[eff].type][0]
            apply(self._hero,Hstatut[eff].power)
            Hstatut[eff].rounds-=1
            if not Hstatut[eff].rounds:
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
            if c in _Game.actions:
                _Game.actions[c](self._hero)
                if c!="i":
                    self.update_effects() 
                    self._floor.moveAllMonsters()
        
        print("--- Game Over ---")

    def restart(self):
        theGame(self).play()


#********************************* Singleton : *********************************

def theGame(game = _Game()):
    return game