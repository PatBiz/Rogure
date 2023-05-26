
# Ce projet à des chances d'utiliser des fonctionnalités de CPython 3.11.2 .
# Tant qu'on doit pouvoir le valider sur LMS, ces fonctionnalités n'ont pas été intégrés.

'''
Membre du groupe :
    - BIZOT Patrick
    - CAUDRON Timothé
    - GUIARD-DEXET Matthieu
    - VICART Paul
'''


import Initialize
from game import theGame


theGame().buildFloor()
theGame().play()