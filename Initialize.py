
# BUT du module : Ajouter tous les 'packages' que l'on a créé au PATH afin de pouvoir importer leurs 'modules'


#******************************* Importations : ********************************

#Module standard :
import os
import sys
import platform


#******************************** Fonctions : **********************************

def initialize_import () :

    mainPATH = os.getcwd() #Comme exécuté dans main.py ALORS ne renvoie que le path vers main.py

    match platform.system(): 
        case "Windows" :
            slash = "\\"
        case "Linux" :
            slash = "/"


    sys.path.append(mainPATH)                       #On ajoute déjà le mainPATH
    sys.path.append(f'{mainPATH}{slash}utils')      #On ajoute le path pour le package 'utils'
    sys.path.append(f'{mainPATH}{slash}game')       #On ajoute le path pour le package 'game'
    sys.path.append(f'{mainPATH}{slash}gui')        #On ajoute le path pour le package 'gui'


initialize_import()