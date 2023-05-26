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

    # ¤¤¤¤¤¤¤¤¤¤¤¤¤¤ DUNDERS ¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤ #
    def __init__ ( self, c1, c2 ) :
        self.c1 = Coord(min(c1.x , c2.x) , min(c1.y , c2.y)) #¤#
        self.c2 = Coord(max(c1.x , c2.x) , max(c1.y , c2.y))

    def __repr__ (self) :
        return str( [self.c1 , self.c2] )

    def __contains__ (self, o) :
        if isinstance(o , Coord) :
            return (self.c1.x <= o.x <= self.c2.x) and (self.c1.y <= o.y <= self.c2.y) #¤#
        return False


    # ¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤ TOOLS ¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤ #
    def getIterator (self) :
        c0 = self.c1
        while c0 != self.c2 :
            nc0 = Coord( c0.x+1 , c0.y )
            c0 = nc0   if(nc0 in self)else   Coord( self.c1.x , c0.y+1 )
            yield c0
        return self.c2

    def center (self) :
        return Coord ( (self.c1.x + self.c2.x)//2 , (self.c1.y + self.c2.y)//2 )

    def intersect (self, other) :
        return (self.c1.x <= other.c2.x ) and (self.c2.x >= other.c1.x) and (self.c1.y <= other.c2.y) and (self.c2.y >= other.c1.y) #¤#

    def randCoord(self) :
        X = rd.randint(self.c1.x , self.c2.x)
        Y = rd.randint(self.c1.y , self.c2.y)
        return Coord(X , Y)