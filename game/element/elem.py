#******************************* Importations : ********************************

# Built-in modules :
from typing import Optional


#********************************** Classes : **********************************

#-------------------------------------------------------------------------------
#                                   ELEMENT
#-------------------------------------------------------------------------------


class Element : #Classe abstraite
    def __init__ (self , name:str , abbrv:Optional[str]=None, visible=True) :
        self._name = name
        self._abbrv = abbrv or name[0]
        self.visible = visible
    
    def __repr__ (self) :
        return self._abbrv