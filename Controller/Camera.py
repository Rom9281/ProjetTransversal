##Bibliothèques
import cv2,numpy as np,matplotlib.pyplot as plt,signal,os
from multiprocessing import Process
from Model.Peripherique import Peripherique


class Camera(Peripherique,Process):
    def __init__(self,queue_commande, queue_info,sem_start):
        super(Camera, self).__init__()
        self.__queue_commande = queue_commande
        self.__queue_info = queue_info
        self.__sem_start = sem_start
        self.__flag = True

        self.cap = cv2.VideoCapture(0) #1+ cv2.CAP_DSHOW

        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.out = cv2.VideoWriter('output.avi',self.fourcc, 25.0, (640,480))
        self.red_seuil = 150
        self.green_seuil = 150
        self.blue_seuil = 100
        self.liste_THRESH_BINARY=[cv2.THRESH_BINARY,cv2.THRESH_BINARY_INV,cv2.THRESH_BINARY]

    
    def run(self):
        signal.signal(signal.SIGTERM, self.signal_handler)

        print("[$] %s:%s : Process Camera actif"%(os.getppid(),os.getpid()))

        self.__sem_start.release()

        while self.__flag:
            # Mettre ce qui se passe en un tour
            pass
            # COde ici
            self.recupererMesure()

            # envoyer les informations
        
        self.cap.release() # Permet d'eteindre la caméra
        self.out.release()
    
    def signal_handler(self):
        print("[*] Process Corps est arrêté")
        self.__flag = False
        self.__sem_start.release()

    def matrice_couleur(self,image,k):
        return image[:,:,k]
        
    def deconstruction(self,image):
        image_red = self.matrice_couleur(image,2)
        image_green = self.matrice_couleur(image,1)
        image_blue = self.matrice_couleur(image,0)
        return image_red,image_green,image_blue
        
    def reconstruction(self,image_red,image_green,image_blue):
        n_ligne = len(image_red)
        n_colonne = len(image_red[0])
        image = []
        for i in range(n_ligne):
            ligne =[]
            for j in range(n_colonne):
                color_b = image_blue[i][j]
                color_g = image_green[i][j]
                color_r = image_red[i][j]
                ligne.append([color_b,color_g,color_r])
            image.append(ligne)
        image_uint8 = np.array(image,dtype=np.uint8)
        return image_uint8

    def reconstruction_seuil(self,image_red,image_green,image_blue):
        n_ligne = len(image_red)
        n_colonne = len(image_red[0])
        image = []
        for i in range(n_ligne):
            ligne =[]
            for j in range(n_colonne):
                color_b = image_blue[i][j]
                color_g = image_green[i][j]
                color_r = image_red[i][j]
                
                ligne.append(min(color_b,color_g,color_r))
            image.append(ligne)
        image_uint8 = np.array(image,dtype=np.uint8)
        return image_uint8

    def reconstruction_seuil_v2(self,image_red,image_green,image_blue):
        new_image = np.multiply(np.multiply(image_red,image_green),image_blue)
        return new_image
        
    def distance_2_points(self,a,b):
        xa=a[0]
        ya=a[1]
        xb=b[0]
        yb=b[1]
        dist = np.sqrt((xa-xb)**2+(ya-yb)**2)
        return dist
        
    def perimetre(self,contour):
        n=len(contour)
        res=self.distance_2_points(contour[0][0],contour[n-1][0])
        for k in range(n-1):
            res += self.distance_2_points(contour[k][0],contour[k+1][0])
        return res
        
    def aire(self,c,image):
        imin = np.min(c[:,:,0])
        imax = np.max(c[:,:,0])
        jmin = np.min(c[:,:,1])
        jmax = np.max(c[:,:,1])
        res=0
        for i in range(imin,imax+1):
            
            for j in range(jmin,jmax+1):
                if (image[j][i]==0):
                    res+=1
        return res

    def aire_v2(self,c,image):
        imin = np.min(c[:,:,0])
        imax = np.max(c[:,:,0])
        jmin = np.min(c[:,:,1])
        jmax = np.max(c[:,:,1])
        petite_image =self.image_seuil[jmin:jmax+1,imin:imax+1]/255
        petite_image_inverse = 1 - petite_image
        res=sum(sum(petite_image_inverse))
        return res
        
    def aire_v3(self,c,image):
        imin = np.min(c[:,:,0])
        imax = np.max(c[:,:,0])
        jmin = np.min(c[:,:,1])
        jmax = np.max(c[:,:,1])
        petite_image =image_seuil[jmin:jmax+1,imin:imax+1]
        res = sum(sum(petite_image == 0))
        return res
        
    def circularite(self,contour,image):
        p=self.perimetre(contour)
        a=self.aire_v3(contour,image)
        return 4*np.pi*a/(p**2)

    def Est_un_cercle(self,c,image,seuil_circularite):
        imin = np.min(c[:,:,0])
        imax = np.max(c[:,:,0])
        jmin = np.min(c[:,:,1])
        jmax = np.max(c[:,:,1])
        p=self.perimetre(c)
        a=self.aire_v3(c,image)
        r=np.sqrt(self.aire_v3(c,image)/np.pi)
        res = (self.circularite(c,image) >= seuil_circularite) and (self.aire_v3(c,image_seuil)>2000) and (perimetre(c)>300)  and (abs(2*(imax-imin)+2*(jmax-jmin) - 8*np.sqrt(aire_v3(c,image_seuil)/np.pi)) < 20 )
        #((circularite(c,image_seuil) >= seuil_circularite) and (aire_v3(c,image_seuil)>2000) and (perimetre(c)>300) and (abs(2*(imax-imin)+2*(jmax-jmin) - 8*np.sqrt(aire_v3(c,image_seuil)/np.pi)) < 20 ))
        return res
        
    def detection_cercle_color(self,image,red_seuil,green_seuil,blue_seuil,liste_THRESH_BINARY):
        image_red,image_green,image_blue = self.deconstruction(image)
        ret,image_red_seuil = cv2.threshold(image_red,red_seuil,255,liste_THRESH_BINARY[0]) #Tresh_Binary, il faut être plus grand que le seuil pour mettre à 1 (en blanc)
        ret,image_green_seuil = cv2.threshold(image_green,green_seuil,255,liste_THRESH_BINARY[1]) #Tresh_Binary_Inv, il faut être plus petit que le seuil pour mettre à 255 (en blanc)
        ret,image_blue_seuil = cv2.threshold(image_blue,blue_seuil,255,liste_THRESH_BINARY[2])
        
        image_seuil = self.reconstruction_seuil_v2(image_red_seuil,image_green_seuil,image_blue_seuil)   
        kernel = np.ones((10, 10), np.uint8)
        image_seuil = cv2.morphologyEx(image_seuil, cv2.MORPH_CLOSE, kernel)
        image_seuil = cv2.morphologyEx(image_seuil, cv2.MORPH_OPEN, kernel)
        
        contours, hierarchy = cv2.findContours(image_seuil, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        frame_contours = self.frame.copy()
        cv2.drawContours(frame_contours,contours,-1,(128,255,128),3)
        
        new_contours = []
        seuil_circularite = 0.80
        
        if (len(contours) != 0):
            for c in contours:
                if self.Est_un_cercle(c,image_seuil,seuil_circularite):
                    new_contours.append(c)
                    
        frame_cercle = self.frame.copy()
        cv2.drawContours(frame_cercle,new_contours,-1,(128,255,128),3)
        
        return image_red_seuil,image_green_seuil,image_blue_seuil,image_seuil,frame_contours,frame_cercle
    

    def recupererMesure(self):
        # Boucle while lance dans le run
        # while( cap.isOpened() ):
            
        ret, frame = self.cap.read()

        if ret == True:
            frame = cv2.flip(frame,1)
            self.out.write(frame)
            cv2.imshow('frame' , frame)
            image_red_seuil,image_green_seuil,image_blue_seuil,image_seuil,frame_contours,frame_cercle =detection_cercle_color(frame,red_seuil,green_seuil,blue_seuil,liste_THRESH_BINARY)
            #print('New appel fonction')
            cv2.imshow('Seuil rouge',image_red_seuil)
            cv2.imshow('Seuil vert',image_green_seuil)
            cv2.imshow('Seuil bleu',image_blue_seuil)
            cv2.imshow('Image color seuil',image_seuil)
            cv2.imshow('Image avec contours',frame_contours)
            cv2.imshow('Image avec cercles',frame_cercle)
            #detection_cercle_color(red_seuil,green_seuil,blue_seuil,liste_THRESH_BINARY)
            """
            # Utile si on est dans la boucle while
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            """
        else:
            print("[$] Caméra non détéctée")
            self.__flag = False

        

    #cv2.destroyAllWindows()
    """
    cv2.imshow('Seuil rouge',image_red_seuil)
    cv2.imshow('Seuil vert',image_green_seuil)
    cv2.imshow('Seuil bleu',image_blue_seuil)
    cv2.imshow('Image color seuil',image_seuil)
    cv2.imshow('Image avec contours',frame_contours)
    cv2.imshow('Image avec cercles',frame_cercle)
    """