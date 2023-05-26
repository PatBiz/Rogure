# *** Importations ***

# Module standard :
import tkinter as tk
#import pillow as pil # --> Nécessite d'importer le module 'pillow'
from functools import partial

#Module perso :
...


def start_Game (win) :

    main_BgColor = 'black'
    #width = 1040 ; height = 600
    win.geometry( f'1040x600+{ (win.winfo_screenwidth() - 1040)//2 }+0' )
    win.config(bg=main_BgColor)

    for widget in win.winfo_children() :
        widget.pack_forget()