#********************************** Classes : **********************************

#-------------------------------------------------------------------------------
#                                    COORD
#-------------------------------------------------------------------------------


class Coord :
    def __init__ (self , x , y) :
        self.x = x
        self.y = y

    # ¤¤¤¤¤¤¤¤¤¤¤¤¤¤ DUNDERS ¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤ #
    def __eq__ (self, other) :
        return self.x == other.x and self.y == other.y

    def __ne__ (self, other) :
        return self.x != other.x or self.y != other.y

    def __repr__ (self) :
        return f"<{self.x},{self.y}>"

    def __add__ (self, other) :
        return Coord(self.x+other.x , self.y+other.y)

    def __sub__ (self, other) :
        return Coord(self.x-other.x , self.y-other.y)

    # ¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤ TOOLS ¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤ #
    def distance (self, other) :
        c = self - other
        return abs(complex(f"{c.x}{'+' if c.y>=0 else ''}{c.y}j"))

    def direction (self, other) :
        o = self-other
        v = o.x / self.distance(other)

        if v > 1/(2**(1/2)) :
            return Coord(-1,0)
        elif v < -1/(2**(1/2)) :
            return Coord(1,0)
        elif o.y > 0 :
            return Coord(0,-1)
        else :
            return Coord(0,1)
    
    @staticmethod
    def isTooFar (pos1, pos2, dist) :
        return round(pos1.distance(pos2)) >= dist