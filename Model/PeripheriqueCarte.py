"""
CPE Lyon 

Projet Transversal

Groupe B1

Romain GAUD, Fares Zaghouane
"""

"""
Objet etant en peripherie d'une carte connectée à la Pi
Connection au deuxième degré
Possède une carte a qui passer des instructions pour se faire activer
"""
from Model.Carte import Carte
class PeripheriqueCarte() :
    
    def __init__(self,carte, codeCommande='',arg1 = 0 ,arg2 = 0) -> None:
        self._carte = carte
        self._code_commande = codeCommande
        self._arg1 = arg1
        self._arg2= arg2
        self._commande = ""

        
    def creerCommande(self) -> str:
        self.__commande = f"{self._code_commande} : {self._arg1} : {self._arg2}\n"
        return self.__commande
    
    def validationCommande(self) -> bool:
        self._carte.valider(self._commande)


if __name__ == "__main__":

    testPeriph = PeripheriqueCarte(0, "PSTSRV", 0, 0)
    print( testPeriph._creerCommande())
