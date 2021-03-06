"""
Code pour le lidar:
Maxime - Romain
"""

# Bibliothèques exterieurs
import matplotlib.pyplot as plt, json, signal, os, time
import rplidar

# Internes
from Model.Peripherique import Peripherique


class Lidar(Peripherique):
    def __init__(self):
        super(Lidar, self).__init__()
        self.__flag = True
        self._pin = "COM8"
        self._connect()
        
    """
    Permet la connection au lidar en utilisant la bibliotheque
    Retourne un objet RPLidar ou None
    """
    def _connect(self) -> rplidar.RPLidar:
   

        try:
            self._serial = rplidar.RPLidar(self._pin)
            print(f"[$] Info Lidar : {self.getInfo()}")
            print(f"[$] Santé Lidar : {self.getHealth()}")
        except rplidar.RPLidarException:
            print("[$] Failed to connect to the Lidar")


    
    def getInfo(self):
        return self._serial.get_info()

    def getHealth(self):
        return self._serial.get_health()
    
    def recupererMesures(self) -> list:
        for scan in self._serial.iter_scans():
            break 

        return scan
    
    def envoyerMesures(self) -> str:
        new_list = []
        ret = ""
        self.__flag = True
        
        while self.__flag:
            try: 
                t1 = time.time()
                self.__flag = False
                ret = self.__cleanData(self.recupererMesures())
                ret = ':'.join(ret)
                t2 = time.time()
                print(f"Time : {t2-t1}")
            except:
                print("\n[$] RPLidarException : Starting Byte Error - Nouvelle Tentative")
    
        return ret
    
    def __cleanData(self,data):
        clean_data = []

        for coord in data:
            clean_data.append(f"{coord[0]},{coord[1]},{coord[2]}")

        return clean_data
    
"""
    Permet de gerer l'interruption du programme LidarIntel
    
    def signal_handler(self,signum,frame):
        print("[*] Process LidarIntel est arrêté")
        self.__flag = False
        
    def __reax(self,ax):
        ax.grid(True)
        ax.spines['left'].set_position('zero')
        ax.spines['right'].set_color('none')
        ax.spines['bottom'].set_position('zero')
        ax.spines['top'].set_color('none')

    def displayIHM(self):
        plt.ion()

        fig = plt.figure()
        ax1 = fig.add_subplot(211)

        ax2 = fig.add_subplot(212)


        for i, scan in enumerate(self._serial.iter_scans()):
        #print('%d: Got %d measurments' % (i, len(scan)))

            if(len(scan)>200):
                data = self.__cleanData(scan,13)
                X,Y,Theta,R = self.__polarToCartesian(data)

                ax1.clear()
                ax2.clear()

                self.__reax(ax1)

                ax1.plot(X, Y, 'b-')
                ax2.plot(Theta, R, 'r-')
                fig.canvas.draw()
                fig.canvas.flush_events()
                #time.sleep(0.4)

    def __polarToCartesian(self,data):
        data = self.__cleanData(data)
        X = []
        Y = []
        Theta= []
        R = []

        for coord in data:
            X.append(coord[1]*math.cos(np.radians(coord[0])))
            Y.append( coord[1]*math.sin(np.radians(coord[0])))
            Theta.append(coord[0])
            R.append(coord[1])

        return X,Y,Theta,R
"""