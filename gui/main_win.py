# *** Importations ***

# Module standard :
import tkinter as tk
#import pillow as pil # --> Nécessite d'importer le module 'pillow'
from functools import partial

#Module perso :
from wins import start_Game


"""Note : (à retirer plus tard) :

Ecran - Détails (PC de Patrick) :
            width  :: 1366
            height :: 768
"""


"Création de la fenêtre principale (de démarrage) :"

mainWin = tk.Tk()
main_BgColor = 'gray'
#icon = tk.PhotoImage(file='win_elmts/rogure_icone.png')

mainWin.geometry( f'740x600+{(mainWin.winfo_screenwidth() - 740)//2}+0')  ;  mainWin.resizable(width=False, height=False)
mainWin.title('Rogure') ; mainWin.iconbitmap(True, 'win_elmts/rogure_icone.ico') ; mainWin.config(bg=main_BgColor)


# Titre :
#img = tk.PhotoImage(file='brain.png')
Title_Label = tk.Label(mainWin,
                    text="Rogure",
                    bg=main_BgColor,
                    width= 20,
                    font=("Arial" , 24 , "bold")
                    #relief= tk.SUNKEN,
)
Title_Label.pack()

# Bouton Start :
Starting_Button = tk.Button(mainWin,
                            text='Start',
                            font=("Arial" , 20 , "bold"),
                            bg='lightgreen',
                            command=partial(start_Game , mainWin),
                            activebackground='green',
                            activeforeground='white',
)
Starting_Button.pack()



mainWin.mainloop()
