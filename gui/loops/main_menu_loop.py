import pygame


from gui.button_actions import quit_rogure
from gui.pygame_utils import find_button_pressed

import env_var as ev


def mainMenuLoop (screen) :

    for button in ev.listButtons :
        screen.blit(button.img, button.rect)
    pygame.display.flip()

    mouse_pos = pygame.mouse.get_pos()
    for button in ev.listButtons :
        if button.rect.collidepoint(mouse_pos) :
            screen.blit(button.active_img, button.rect)
            pygame.display.update(button.rect)

    for event in pygame.event.get() :

        if event.type == pygame.QUIT : #On ferme la fenêtre + stoppe le jeu
            quit_rogure()

        elif event.type == pygame.MOUSEBUTTONDOWN :
            button = find_button_pressed(ev.listButtons, event.pos)
            if button :
                try : screen.blit(button.active_img, button.rect)
                except AttributeError : pass 
                pygame.display.update(button.rect)
                button.action()
        
        #NON
        """ 
        elif event.type == pygame.K_UP : # Objectif : Arriver à faire le petit effet ::
            
            try :
                button_active += 1
                button = ev.listButtons[button_active]
                screen.blit(button.active_img, button.rect)
                pygame.display.update(button.rect)

            except IndexError :
                button_active = 0
                button = ev.listButtons[0]
                screen.blit(button.active_img, button.rect)
                pygame.display.update(button.rect)
        """

    pygame.display.flip()