from .main_menu_loop import mainMenuLoop
from .game_loop import gameLoop, inventoryLoop
#from .loading_loop import *
#from .saving_loop import *
#from .shopping_loop import *
from .death_screen_loop import deathScreenLoop


__all__ = (
    "mainMenuLoop",
    "gameLoop",
    "inventoryLoop",

    "deathScreenLoop",
)