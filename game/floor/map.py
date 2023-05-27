#******************************* Importations : ********************************

# Built-in modules :
from typing import Optional
import random as rd

# Modules persos :
import game._game as Gme
from .coord import Coord
from .room import Room
import element as Elmt #Obligé de l'importer ainsi car 'element' a besoin de 'game' qui lui même a besoin de 'map' => "circular import"

from utils import statically_typed_function


#********************************** Classes : **********************************

#-------------------------------------------------------------------------------
#                                     MAP
#-------------------------------------------------------------------------------


class Map :

    # ¤¤¤¤¤¤¤¤¤¤ CLASS ATTRIBUTES ¤¤¤¤¤¤¤¤¤¤ #
    empty = ' '
    ground = '.'
    wall = '#'
    dir = {'z': Coord(0,-1) , 's': Coord(0,1) , 'd': Coord(1,0) , 'q': Coord(-1,0)}


    # ¤¤¤¤¤¤¤¤¤¤¤¤¤¤ DUNDERS ¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤ #
    "REMARQUE : Certains 'dunders' font appel à des 'tools'"
    @statically_typed_function
    def __init__ (self, size: Optional[int] =20, pos: Optional[Coord] =Coord(1,1), nbRooms: Optional[int] =7, hero: Optional[Elmt.Hero] =None) :  #########

        self.size = size
        self._mat = [[Map.empty]*size for _ in range (size)]
        self._elem = {}
        self._cache = {} #Cache d'objet qui va se faire 'piétiner'
        #self._mat[posHeroDepart.y][posHeroDepart.x] = self._hero

        self._rooms = []
        self._roomsToReach = []
        #''''''''''''''''''''''''''
        self.generateRooms(nbRooms)
        self.reachAllRooms()
        self.putWall()
        for r in self._rooms :
            self.decorateRoom(r)
        #..........................

        self.posHeroDepart = self._rooms[0].center()
        self._hero = hero or Elmt.Hero()
        #''''''''''''''''''''''''''
        self.put_Elmt_At_Coord(self._hero , self.posHeroDepart)
        #..........................
        
    def __repr__ (self) :
        s = ""
        for line in self._mat :
            try :
                s += "".join(line) + '\n'
            except TypeError: #S'execute SI type(element de la ligne) != str
               s += "".join([str(i) for i in line]) + '\n'
        return s

    def __len__ (self) :
        return self.size
        
    def __contains__ (self, o) :
        #Si o est une coordonnée
        if isinstance(o , Coord) :
            return o.x<len(self) and o.x>=0 and o.y<len(self) and o.y>=0
        #Si o est un élément
        if isinstance(o , Elmt.Element) :
            return o in self._elem.keys()
        return False

    def __getitem__ (self, key) :
        if isinstance(key , Coord) :
            return self.get_Elmt_At_Coord(key)

        if isinstance(key , Elmt.Element)  :
            return self.get_Pos_Of_Elmt(key)

        raise TypeError

    def __setitem__ (self, key, value) : #Pour éviter de dupliquer un élément (On part du principe POUR L'INSTANT que chaque Element est UNIQUE)

        if isinstance(key, Coord) and isinstance(value, Elmt.Element) :
            if value in self :
                self.remove_Elmt_At_Coord(self[value])
            self.put_Elmt_At_Coord(value , key)
            return
     
        if isinstance(key, Elmt.Element) and isinstance(value, Coord) :
            if key in self :
                self.remove_Elmt_At_Coord(self._elem[key])
            self.put_Elmt_At_Coord(key , value)
            return

        raise TypeError

    def __delitem__ (self, item):
        if isinstance(item , Coord) :
            self.remove_Elmt_At_Coord(item)
            return

        if isinstance(item , Elmt.Element) :
            self.remove_Elmt_At_Coord(self[item])
            return

        raise TypeError


    # ¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤ TOOLS ¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤ #
    "REMARQUE : J'ai changé les noms de certaines méthodes pour des nom plus parlant. Mais les anciens noms fonctionnent aussi."
    @statically_typed_function
    def get_Elmt_At_Coord (self, coord:Coord) :
        """ Renvoie l'élément aux coordonnées données 'coord' """
        if coord not in self :
            raise IndexError('Out of map coord')
        return self._mat[coord.y][coord.x]
    get = get_Elmt_At_Coord

    @statically_typed_function
    def get_cachedItem_At_Coord (self, coord:Coord) :
        for item in self._cache :
            if self[item] == coord :
                return item

    @statically_typed_function
    def get_Pos_Of_Elmt (self, elem:Elmt.Element) :
        """ Renvoie la position de l'élément données 'elem' """
        if elem in self :
            return self._elem[elem]
    pos = get_Pos_Of_Elmt

    @statically_typed_function
    def put_Elmt_At_Coord (self, elem:Elmt.Element, coord:Coord) :
        """ Place l'élément 'elem' aux coordonnées 'coord' """
        if coord not in self :
            raise IndexError('Out of map coord')
        if self.get_Elmt_At_Coord(coord) != Map.ground :
            raise ValueError(f"Incorrect cell. Cell was occupied by '{self.get_Elmt_At_Coord(coord)}'")
        if elem in self :
            raise KeyError('Already placed')
        self._mat[coord.y][coord.x] = elem
        self._elem[elem] = coord
    put = lambda self,coord,elem : self.put_Elmt_At_Coord (elem , coord)

    @statically_typed_function
    def remove_Elmt_At_Coord (self, coord:Coord) :
        """ Retire l'élément aux coordonnées données 'coord' """
        if coord in self :
            self._mat[coord.y][coord.x] = Map.ground
            del self._elem[list(self._elem.keys())[list(self._elem.values()).index(coord)]]
            return #Pour clôre la méthode
        raise IndexError('Out of map coord')
    rm = remove_Elmt_At_Coord

    def getIterator_coord (self) :
        return Room(Coord(0 , 0), Coord(self.size-1 , self.size-1)).getIterator()
    
    def getIterator_elmt (self) :
        for c in self.getIterator_coord() :
            yield self.get_Elmt_At_Coord(c)


    # ¤¤¤¤¤¤¤¤¤¤¤ TOOLS BY TYPES ¤¤¤¤¤¤¤¤¤¤¤ #
    #------------- COORD :

    @statically_typed_function
    def projette_In_Map (self, C:Coord) :
        """ Projette une coordonées HORS map dans la map """
        if C not in self :
            c1 = self.c1 ; c2 = self.c2
            if C.x <= c1.x :
                C =         c1           if(C.y <= c1.y)else   Coord(c1.x , c2.y)  if(C.y >= c2.y)else   Coord(c1.x , C.y)
            elif C.x >= c2.x :
                C = Coord(c2.x , c1.y)   if(C.y <= c1.y)else           c2          if(C.y >= c2.y)else   Coord(c1.x , C.y)
            else :
                C = Coord(C.x , c1.y)    if(C.y <= c1.y)else   Coord(C.x , c2.y)
        return C
    
    #------------- ROOM :

    @statically_typed_function
    def findRoom (self, coord:Coord) :
        """Cherche la salle contenant la coordonnée 'coord'"""
        if self[coord] == Map.ground :
            for room in self._roomsToReach :
                if coord in room :
                    return room
        return False

    @statically_typed_function
    def intersectNone(self, room:Room) :
        """Regarde SI aucunes salles dans '_roomsToReach' se coupent"""
        return not (any(room.intersect(room2) for room2 in self._roomsToReach ))

    @statically_typed_function
    def addRoom (self, room:Room):
        """Ajoute une salle dans la map"""
        self._roomsToReach += [room]

        c0 = room.c1
        while c0 != room.c2 :
            self._mat[c0.y][c0.x] = Map.ground
            nc0 = Coord( c0.x+1 , c0.y )
            c0 = nc0   if(nc0 in room)else   Coord( room.c1.x , c0.y+1 )
        self._mat[c0.y][c0.x] = Map.ground

    #-------------- ITEM :

    @statically_typed_function
    def cacheItem (self, item:Elmt.Item) :
        if item not in self :
            raise ValueError(f"'{item}' is not in map")
        self._cache[item] = self.get_Pos_Of_Elmt(item)

    @statically_typed_function
    def cacheItem_At_Coord (self, item:Elmt.Item, coord:Coord) :
        self._cache[item] = coord

    @statically_typed_function
    def uncacheItem (self, item:Elmt.Item) :
        if self._cache :
            itemPosition = self._cache[item]
            try : self.put_Elmt_At_Coord(item, itemPosition)
            except ValueError : pass
            else : del self._cache[item]

    def uncacheAllItem (self) :
        for item in list(self._cache) :
            self.uncacheItem(item)


    # ¤¤¤¤¤¤ METHODES DE CONSTRUCTION ¤¤¤¤¤¤ #
    # --- Génération des salles ---

    def randRoom (self) :
        x1 = rd.randint(0,len(self)-3)
        y1 = rd.randint(0,len(self)-3)

        c1 = Coord(              x1              ,                y1              )
        c2 = Coord( min( x1+rd.randint(3,8) , len(self)-1 ) , min( y1+rd.randint(3,8) , len(self)-1 ) )
        return Room(c1 , c2)

    @statically_typed_function
    def generateRooms(self, n:int) :
        for _ in range(n) :
            r = self.randRoom()
            if self.intersectNone(r) :
                self.addRoom(r)

    # --- Plaçage du sol ---

    @statically_typed_function
    def dig(self, coord:Coord) :
        """Pose du sol à 'coord' ET retire la salle qui contient 'coord'"""
    
        #Place du sol à coord
        self._mat[coord.y][coord.x] = Map.ground

        #Retire la salle qui contient le point de coordonnée 'coord'
        if r := self.findRoom(coord):
            self._roomsToReach.pop(self._roomsToReach.index(r))
            self._rooms.append(r)

    @statically_typed_function
    def corridor (self, start:Coord, end:Coord) :
        """Relie 2 points entre eux"""

        #Il faudrait tester que 'start' et 'end' soit dans la map

        c0 = self.projette_In_Map(start)
        wY = Map.dir['s']   if(start.y<end.y)else   Map.dir['z']
        wX = Map.dir['d']   if(start.x<end.x)else   Map.dir['q']
        try :
            while c0.y != end.y :# and c0 in self  :
                self.dig(c0)
                c0 += wY
            while c0.x != end.x :# and c0 in self :
                self.dig(c0)
                c0 += wX
            self.dig(c0)
        except IndexError : pass # Si on est plus dans la map alors on s'arrète. 'try...except' évite de tjrs vérifier si on est dans la map

    def reach (self) :
        """Relie 2 salle ALEATOIREMENT"""

        A = rd.choice(self._rooms)
        B = rd.choice(self._roomsToReach)
        self.corridor (A.center() , B.center())

    def reachAllRooms (self) :
        self._rooms.append(self._roomsToReach.pop(0))
        while self._roomsToReach :
            self.reach()

    # --- Plaçage des murs ---

    def putWall (self) :
        for c in self.getIterator_coord() :
            if self[c] == Map.ground :
                #Place des murs autour de 'c' dans les cases vides
                for c2 in [Coord(c.x+1,c.y), Coord(c.x+1,c.y+1), Coord(c.x+1,c.y-1), Coord(c.x-1,c.y), Coord(c.x-1,c.y+1), Coord(c.x-1,c.y-1),  Coord(c.x,c.y+1), Coord(c.x,c.y-1)] :
                    if c2 in self  and  self[c2] == Map.empty :
                        self._mat[c2.y][c2.x] = Map.wall

    # --- Plaçage des créatures ---

    def randEmptyCoordInRoom(self, r) :
        """
        Ancien nom : 'randEmptyCoord'
        Ancien emplacement : classe 'Room'
        """
        c = r.randCoord()
        while self.get_Elmt_At_Coord(c) is not Map.ground  or  c==r.center():
            c = r.randCoord()
        return c

    def decorateRoom(self, r) :
        """
        Ancien nom : 'decorate'
        Ancien emplacement : classe 'Room'
        """
        self.put(self.randEmptyCoordInRoom(r) , Gme.theGame().randEquipment())
        self.put(self.randEmptyCoordInRoom(r) , Gme.theGame().randMonster())

    # ¤¤¤¤¤¤¤ METHODES DE DEPLACEMENT ¤¤¤¤¤¤ #

    def moveAllMonsters(self) :
        for monster in list(self._elem) :
            #Si ce n'est pas une créature
            if type(monster) != Elmt.Monster : 
                continue

            #Si le héro est trop loin
            orig = self[monster] #Position de actuelle du monstre
            if orig.distance(self[self._hero]) > 6 : 
                continue

            dest = orig + orig.direction(self[self._hero])
            if (dest in self)  and  ((objMet := self[dest]) != Map.wall)  and  (objMet != Map.empty) :
                print(f"{monster}-->{objMet}")
                if objMet == Map.ground:
                    self[monster] = dest
                elif Elmt.meet(monster, objMet) :
                    self.remove_Elmt_At_Coord(dest)       #On vide l'emplacement de l'élément
                    self[monster] = dest

    @statically_typed_function
    def moveHero(self, hero:Elmt.Hero, direc:Coord):
        orig = self[hero]
        dest = orig + direc       
        if (dest in self)  and  ((objMet := self[dest]) != Map.wall)  and  (objMet != Map.empty) :
            print(f"{hero}-->{objMet}") ##
            if objMet == Map.ground :
                self.remove_Elmt_At_Coord(orig)       #On vide l'ancien emplacement
                self.put_Elmt_At_Coord(hero , dest)      #On déplace 'e' en 'nc'
            elif Elmt.meet(self._hero, objMet) :
                self.remove_Elmt_At_Coord(dest)       #On vide l'emplacement de l'élément
                self[hero] = dest