import pygame


from pygame_utils import GameClosureException, Trigger

import win_init

#-------------------------------------------------------------------------------
#                                  MAIN MENU
#-------------------------------------------------------------------------------


def start_rogure (screen):
    print ("Start")
    return Trigger.InGame, win_init.gameInit(screen)

def load_rogure (screen) :
    print ("Load")
    return Trigger.InLoading#, win_init.loadInit(screen)

def quit_rogure () :
    print ("Quit")
    pygame.quit()
    raise GameClosureException("Player has closed the game.")


#-------------------------------------------------------------------------------
#                                  GAME
#-------------------------------------------------------------------------------

def open_inventory (screen) :
    print("Open Inventory")
    return Trigger.InInventory, win_init.inventoryInit(screen)

# ------- Inventory :

def close_inventory (screen):
    print("Close Inventory")
    return Trigger.InGame, win_init.gameInit(screen)

def equip (screen, item_indice) : #Si clic inventaire
    print(f"Equipping Item{item_indice}")
    return ...

# ------- Shop :

def goto_shop () :
    ...