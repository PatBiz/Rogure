from gui.pygame_utils import Printer
from game import theGame


" Constantes d'environnement : "

game    = theGame()
printer = Printer(pos=(0,-80), lmove=80)

" Variables d'environnement : "

status      : str
listButtons : list
listMapCell : list