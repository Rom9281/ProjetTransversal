from abc import ABC, abstractmethod

class Capteur(ABC):
    
    @abstractmethod
    def recupererMesure(self):
        pass
