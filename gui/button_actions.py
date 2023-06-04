import pygame


from pygame_utils import GameClosureException, Trigger
import win_init
import env_var as ev

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

def equip (screen, item_indice) : #Si clic inventaire
    print(f"Equipping Item{item_indice}")
    ...

def disequip (screen, item) :
    print(f"Disequipping {item._name}")
    ...

# ------- Shop :

def goto_shop () :
    print("Start shopping")

    ...

#-------------------------------------------------------------------------------
#                              DEATH SCREEN
#-------------------------------------------------------------------------------

def restart_rogure (screen) :
    print("Restart Rogure")
    ...
    win_init.gameInit(screen)


def back_to_menu (screen) :
    print("Back to menu")
    win_init.mainMenuInit(screen)