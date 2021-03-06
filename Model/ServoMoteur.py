"""
CPE Lyon 

Projet Transversal

Groupe B1

Romain GAUD, Fares Zaghouane
"""

from http.client import FAILED_DEPENDENCY

from Model.PeripheriqueCarte import PeripheriqueCarte
from Model.Carte import Carte


class ServoMoteur(PeripheriqueCarte) :
    
    def __init__(self,carte, axe = 0) -> None:
        # axe correspond au servo Horizontal(0) ou vertical(1)
        super().__init__(carte,"PSTSRV",axe ,0)  
        self.__angle = 0
        self.__gauche = True
        
    def getAngle(self)-> int:
        return self.__angle
    
    def getOrientation(self)-> int:
        return self._arg1
    
    def rotation(self, angle : int) -> bool:
        # angle correspond a l'angle que l'on veux donner [0 : 180]
        valideMouvement = False
        if ( 0 <= angle <= 180):
            self.__angle = angle
            self.arg2 = self.__angle
            self.__carte.ecrireCommand(self.creerCommande())
            valideMouvement = self.validationCommande()
        return valideMouvement
    
    def auto(self):
        if (self.__gauche == True) :
            if not (self.rotationGauche(5)):
                self.__gauche = False
        else:
            if not (self.rotationDroite(5)):
                self.__gauche = True

    
    def rotationGauche(self,angle : int) -> bool:
        return self.rotation(self.__angle+angle)
    
    def rotationDroite(self,angle : int) -> bool:
        return self.rotation(self.__angle-angle)

   
    # fonctions petit mouvement correspond a un mouvement d'un valeur predefinie : 5°
    def petiteRotationAjout(self) -> bool:
        valideMouvement = False
        if (self.__angle + 5 <=180 ):
            self.__angle += 5
            self.arg2 = self.__angle
            self.__carte.ecrireCommand(self.creerCommande())
            valideMouvement = self.validationCommande()
        
        return valideMouvement

    def petiteRotationRetire(self) -> bool:
        valideMouvement = False
        if (self.__angle - 5 >= 0 ):
            self.__angle -= 5
            self.arg2 = self.__angle
            self.__carte.ecrireCommand(self.creerCommande())
            valideMouvement = self.validationCommande()
        
        return valideMouvement



    # def petitMouvVerHaut(self):
    #     return self.mouvement(self.__angle_ver + 10)

    # def petitMouvVerBas(self):
    #     return  self.mouvement(self.__angle_ver - 10)

    # def petitMouvHorDrt(self):
    #     return self.mouvement(self.__angle_hor + 10)

    # def petitMouvHorGch(self):
    #     return self.mouvement(self.__angle_hor - 10)


    # def mouvementHorizontal(self,angle):
    #     self._arg1 = "0"
    #     self._arg2 = str(angle)
    #     self._carte.ecrireCommand(self._creerCommande())
    #     self.__angle_hor = angle
    #     return self._carte.valider(self._commande)
    
    # def mouvementVertical(self,angle):
    #     self._arg1 = "1"
    #     self._arg2 = str(angle)
    #     self._carte.ecrireCommand(self._creerCommande())
    #     self.__angle_ver = angle
    #     return self._carte.valider(self._commande)

if __name__ == "__main__":
    carte = Carte()
    testServoMoteur = ServoMoteur(carte, 1)

    print(testServoMoteur.getAngle())
    print(testServoMoteur.getOrientation())
    print(testServoMoteur.mouvement(20))
    print(testServoMoteur.getAngle())
