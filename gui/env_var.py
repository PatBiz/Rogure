from gui.pygame_utils import Printer
from game import theGame


" Constantes d'environnement : "

game    = theGame()
printer = Printer(pos=(246,-80), lmove=80)

#Sprites courants :
emptyCell = "gui/assets/Decors/empty.png"
unknownItem = "gui/assets/Items/none_item.png"

" Variables d'environnement : "

status      : str
listButtons : list
listMapCell : list