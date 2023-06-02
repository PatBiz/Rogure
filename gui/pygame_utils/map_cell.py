class MapCell :
    def __init__(self, img, coord) :
        self.img = img
        self.coord_in_map = coord
    
    def __repr__ (self) :
        return f"<{self.coord_in_map.x} ; {self.coord_in_map.y}>"
    
def getCell_In_Room (room, lCell) :
    """
    Renvoie la liste des cellule dans la salle 'room'.

    lCell <=> map._mat MAIS conitent des cellule et non des elements
    """
    lCell = [ l[room.c1.x : room.c2.x+1] for l in lCell[room.c1.y : room.c2.y+1] ]

    for _ in range(len(lCell)):
        lCell += lCell.pop(0)

    return lCell