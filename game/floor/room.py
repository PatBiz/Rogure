#******************************* Importations : ********************************

# Built-in modules :
import random as rd

# Modules persos :
from .coord import Coord


#********************************** Classes : **********************************

#-------------------------------------------------------------------------------
#                                    ROOM
#-------------------------------------------------------------------------------


class Room :
    def __init__ ( self, c1, c2 ) :
        self.c1 = Coord(min(c1.x , c2.x) , min(c1.y , c2.y)) #¤#
        self.c2 = Coord(max(c1.x , c2.x) , max(c1.y , c2.y))

    # ¤¤¤¤¤¤¤¤¤¤¤¤¤¤ DUNDERS ¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤ #
    def __repr__ (self) :
        return str( [self.c1 , self.c2] )

    def __contains__ (self, o) :
        if isinstance(o , Coord) :
            return (self.c1.x <= o.x <= self.c2.x) and (self.c1.y <= o.y <= self.c2.y) #¤#
        return False

    def __iter__ (self) :
        c0 = self.c1
        while c0 != self.c2 :
            yield c0
            nc0 = Coord( c0.x+1 , c0.y )
            c0 = nc0   if(nc0 in self)else   Coord( self.c1.x , c0.y+1 )
        yield self.c2

    # ¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤ TOOLS ¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤ #
    def center (self) :
        return Coord ( (self.c1.x + self.c2.x)//2 , (self.c1.y + self.c2.y)//2 )

    def intersect (self, other) :
        return (self.c1.x <= other.c2.x ) and (self.c2.x >= other.c1.x) and (self.c1.y <= other.c2.y) and (self.c2.y >= other.c1.y) #¤#

    def randCoord(self) :
        X = rd.randint(self.c1.x , self.c2.x)
        Y = rd.randint(self.c1.y , self.c2.y)
        return Coord(X , Y)
    

class ShopRoom(Room):
    def __init__(self,c1,c2):
        Room.__init__(self,c1,c2)



class TrapRoom(Room):
    trapTypes={"burned": (lambda creature, power : creature.takeDamage(power), 4),
                "paralized": (lambda a,b : print("Cc"),4), 
                "poisoned": (lambda creature, power : creature.takeDamage(power), 3)}        #Tours +1

    def __init__(self,c1,c2,nbTraps=2,trapTypesUsed=None):
        Room.__init__(self,c1,c2)
        self.nbTraps=nbTraps
        self.trapTypesUsed=trapTypesUsed