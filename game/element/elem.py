#******************************* Importations : ********************************

# Built-in modules :
from typing import Optional


#********************************** Classes : **********************************

#-------------------------------------------------------------------------------
#                                   ELEMENT
#-------------------------------------------------------------------------------


class Element : #Classe abstraite
    def __init__ (self , name:str , abbrv:Optional[str]=None) :
        self._name = name
        self._abbrv = abbrv or name[0]
    
    def __repr__ (self) :
        return self._abbrv