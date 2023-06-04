#******************************* Importations : ********************************

# Built-in modules :
import pygame

#Modules persos :
from pygame_utils import GameClosureException
import win_init
import env_var as ev


#******************************** Fonctions : **********************************

#-------------------------------------------------------------------------------
#                                  MAIN MENU
#-------------------------------------------------------------------------------


def start_rogure (screen):
    print ("Start")
    win_init.gameInit(screen)

def load_rogure (screen) :
    print ("Load")
    #win_init.loadInit(screen)

def quit_rogure () :
    print ("Quit")
    pygame.quit()
    raise GameClosureException("Player has closed the game.")


#-------------------------------------------------------------------------------
#                                  GAME
#-------------------------------------------------------------------------------

def open_inventory (screen) :
    print("Open Inventory")
    win_init.inventoryInit(screen)

# ------- Inventory :

def close_inventory (screen):
    print("Close Inventory")
    win_init.gameInit(screen)

def equip (item_indice) : #Si clic inventaire
    print(f"Equipping Item{item_indice}")
    hero = ev.game.__hero__
    hero.use(hero._inventory[item_indice])

# ------- Shop :

def goto_shop (screen) :
    print("Start shopping")
    win_init.shopInit(screen)

def close_shop (screen):
    print("Close Inventory")
    win_init.gameInit(screen)

def buy (item, price) :
    from copy import copy
    if hero._porte_monnaie >= price :
        hero = ev.game.__hero__
        hero.take(copy(item))
        hero._porte_monnaie -= price