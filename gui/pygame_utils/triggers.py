class Trigger :
    InMainMenu = "in_main_menu"
    InGame = "in_game"
    InLoading = "in_loading"
    InInventory = "in_inventory"
    InShop = "in_shop"
    HasLost = "has_lost"

class GameClosureException (Exception) :
    pass