class Trigger :
    InMainMenu = "in_main_menu"
    InGame = "in_game"
    InLoading = "in_loading"
    InInventory = "in_inventory"
    #InShop = "in_shop" #pas sûr

class GameClosureException (Exception) :
    pass