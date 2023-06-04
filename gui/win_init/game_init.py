#******************************* Importations : ********************************

# Built-in modules :
import pygame
from functools import partial

# Modules persos :
from gui.pygame_utils import Button, InventorySlot, HeroSlot, Trigger, MapCell, InfoBar
from gui.sprite_getter import getFloorSprite, getWallSprite
import button_actions as ba

# Variables d'environnement :
import env_var as ev


#******************************** Fonctions : **********************************

#-------------------------------------------------------------------------------
#                                 GAME INIT
#-------------------------------------------------------------------------------


def _generate_newFloor ():
    ev.__dict__["generateMap"] = False

    # Récupération des variables d'environnements :
    g = ev.game
    ev.game.buildFloor()
    m = g.__floor__

    #Définition des cellules de la map :
    l = []
    lCell = []
    for coord in m.getIterator_coord() :
        char = m.get_Elmt_At_Coord(coord)
        match char :
            case ' ' :
                cell = MapCell(ev.emptyCell , coord)
            case '#' :
                cell = MapCell(getWallSprite(m, coord) , coord)
            case _ :
                cell = MapCell(getFloorSprite() , coord)
        l.append(cell)
        if coord.x == m.size-1 :
            lCell.append( l )
            l = []

    ev.__dict__["listMapCell"] = lCell

def gameInit(screen):
    """ Initialise la fenêtre de jeu ET renvoie la liste des boutons. """ 

    if ev.generateMap:
        _generate_newFloor()


    #Création des autres composants :
    BgGameImage = pygame.image.load("gui/assets/background/inGame_Background.jpg").convert()

    InfoHero = pygame.image.load("gui/assets/background/hero_info_wide.png").convert_alpha()
        
    PvInfoBar = InfoBar("gui/assets/background/health_bar",
                    pos=(78,78),
                    look="_hp",
                    currentAmount=10,
                    fullAmount=10)
    
    ManaInfoBar = InfoBar("gui/assets/background/mana_bar",
                    pos=(78,105),
                    look="_hp", #"_mana",
                    currentAmount=10,
                    fullAmount=10)
    
    SatietyInfoBar = InfoBar("gui/assets/background/satiety_bar",
                    pos=(78,132),
                    look="_hp", #"_satiety",
                    currentAmount=10,
                    fullAmount=10)

    backPackButton = Button(path="gui/assets/Buttons/in_game/inventory_btn.jpg",
                    pos=(151,155),
                    action=partial(ba.open_inventory, screen),
                    alpha=False)

    screen.blit(BgGameImage, (-200,-50))
    screen.blit(InfoHero, (0,0))
    screen.blit(PvInfoBar.img, PvInfoBar.rect)
    screen.blit(ManaInfoBar.img, ManaInfoBar.rect)
    screen.blit(SatietyInfoBar.img, SatietyInfoBar.rect)
    screen.blit(backPackButton.img, backPackButton.rect)
    pygame.display.flip()

    pygame.event.pump()

    # Mises à jour des variables d'environnements
    ev.__dict__["status"] = Trigger.InGame
    ev.__dict__["updateScreen"] = True
    ev.__dict__["updateInfo"] = False
    ev.__dict__["listInfoBar"] = [PvInfoBar, ManaInfoBar, SatietyInfoBar]
    ev.__dict__["listButtons"] = [backPackButton]


#-------------------------------------------------------------------------------
#                              INVENTORY INIT
#-------------------------------------------------------------------------------


def inventoryInit (screen) :
    """ Initialise l'affiche de l'inventaire du joueur ET renvoie la liste des boutons. """

    # Création des composants de la fenêtre :

    PopUpInventory = pygame.image.load("gui/assets/background/inventory_PopUp.png").convert_alpha()
    heroWeaponSlot = HeroSlot(path="gui/assets/Buttons/in_game/inventory/weapon_slot.png",
                             pos=(415, 480),
                             place = "weapon")
    heroHelmetSlot = HeroSlot(path="gui/assets/Buttons/in_game/inventory/helmet_slot.png",
                              pos = (522, 480),
                              place = "helmet")
    heroChestplateSlot = HeroSlot(path="gui/assets/Buttons/in_game/inventory/chestplate_slot.png",
                              pos=(591, 480),
                              place="chestplate")

    lCases = []

    screen.blit(PopUpInventory, (375,70))
    #screen.blit(inventoryButton.img, inventoryButton.rect) # ----- Qd l'inventaire sera un btn

    i = 0
    for k in range (3) :
        for x in [395,490,588,683] :
            lCases.append(InventorySlot(path="gui/assets/Buttons/in_game/inventory/inv-case_btn.png",
                                        pos=(x,147+k*98),
                                        action=partial(ba.equip, screen, i),
                                        invId=i))
            screen.blit(lCases[-1].img, lCases[-1].rect)
            i += 1
    pygame.display.flip()

    ev.__dict__["status"] = Trigger.InInventory
    ev.__dict__["listButtons"] = lCases + []
    ev.__dict__["listSlots"] = [heroWeaponSlot, heroHelmetSlot, heroChestplateSlot]


#-------------------------------------------------------------------------------
#                              SHOP INIT
#-------------------------------------------------------------------------------

def shopInit (screen) :
    """ Initialise l'affiche de l'inventaire du joueur ET renvoie la liste des boutons. """
    import game.element as Elmt

    # Création des composants de la fenêtre :

    PopUpShop = pygame.image.load("gui/assets/background/Shop_PopUp.png").convert_alpha()
    article1 = Button(path="gui/assets/Buttons/in_shop/hp_btn.png",
                            pos=(415, 480),
                            action=partial(ba.buy, Elmt.equipment.Consumables("heal_potion","!",usage=Elmt.heal), 3),
                            alpha=False)
    article2 = Button(path="gui/assets/Buttons/in_shop/tp_btn.png",
                            pos=(522, 480),
                            action=partial(ba.buy, Elmt.equipment.Consumables("teleport_potion","!",usage=lambda hero : Elmt.teleport(hero , unique = True)), 5),
                            alpha=False)
    article3 = Button(path="gui/assets/Buttons/in_shop/d_btn.png",
                            pos=(591, 480),
                            action=partial(ba.buy, Elmt.equipment.ProjectileWeapon("dague",usage=lambda hero,dir: Elmt.capacity.throw(hero,hero._strength,True,dir)), 7),
                            alpha=False)
    
    screen.blit(PopUpShop, (375,70))

    ev.__dict__["listButtons"] = [article1, article2, article3]
    ev.__dict__["status"] = Trigger.InShop