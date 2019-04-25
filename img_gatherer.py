import rosinterface as roscv
import numpy as np
import cv2
import aruco
import probdefs
import observationgenner as obsGen


class img_gather(object):
    def __init__(self,N_cams,arucoModel,calc,Rcam=None):
      
        self.N_cams = N_cams

        self.gatherCounter = [0]*N_cams

        self.gatherReady = np.zeros((N_cams),dtype=np.uint8)

        self.images =  np.zeros((480,640*N_cams,3),dtype=np.uint8)

        self.Allobs = [ [] for i in range(self.N_cams) ]


        self.R = arucoModel['R']
        self.t = arucoModel['t']

        self.calc = calc

        if(self.calc==0):
            print("R problem Definition")
        elif(self.calc==1):
            print("t problem Definition")
        else:
            print("SOMETHING WENT WRONG")

        self.Rcam = Rcam

        self.ATA = np.zeros((N_cams*3,N_cams*3))

        self.ATb = np.zeros((N_cams*3,1)) # *3 because tranlations are 3x1

        #print("obs")
        #print(self.ATA.shape)
        
    def showImg(self):
        cv2.imshow("Image window ",self.images)           
        cv2.waitKey(1)
        #print(self.gatherCounter)
        #pass

    def GatherImg(self,camId,img,obs):
        #print("on gather img")
        self.images[0:480,camId*640:camId*640+640,0:3]=img
        
        #print(np.sum(img-self.images[0:480,camId*640:camId*640+640,0:3]))
        self.gatherCounter[camId] = self.gatherCounter[camId] +1
        
        self.gatherReady[camId]=1

        self.Allobs[camId]=self.Allobs[camId] +obs  # WRONG SHOULD IT BE concantenate lists OR =?


        if(np.sum(self.gatherReady)== self.N_cams):
            
            #print("listu printu")
            #for o in self.Allobs:
            #    print(len(o))
            #Generate Pairs
            obsR , obsT = obsGen.GenerateCameraPairObs(self.Allobs,self.R,self.t)

            if self.calc == 0:
                A = probdefs.rotationProbDef(obsR,self.N_cams)
                #print(ATA.shape)
                self.ATA = self.ATA + np.dot(A.T,A)
            elif self.calc ==1:

                

                A,b =  probdefs.translationProbDef(obsT,self.Rcam,self.N_cams)

                self.ATA = self.ATA + np.dot(A.T,A) #way to save the matrix in a compact manner

                self.ATb = self.ATb + np.dot(A.T,b) #way to save the matrix in a compact manner

            #cleanse
            self.gatherReady = np.zeros((self.N_cams),dtype=np.uint8)

            #clear observations
            self.Allobs = [ [] for i in range(self.N_cams) ]

            #raw_input("DO U KNO Da WAE?")


        



    



            

            
            
        
        




   