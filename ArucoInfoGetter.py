import rosinterface as roscv
import numpy as np
import cv2
import aruco
import probdefs



class ArucoInfoGetter(object):
    def __init__(self):
      
        self.count = 0
        self.Nmarkers = 12 #number of markers, MUST BE CONTIGUOUS for this to work
        self.markerIDoffset=-2 #offset dos markers, como vao do 2 ao 12, o offset e 2

        self.ATA = np.zeros((self.Nmarkers *3,self.Nmarkers *3)) #*3 because rotations matrix is 3x3

        self.ATb = np.zeros((self.Nmarkers *3,1)) # *3 because tranlations are 3x1





    def callback(self,data,args):

        showVid = args[0]["showVideo"]
        K=args[0]["K"]
        D=args[0]["D"]
        R=args[0]["R"] #<-CORRECT, but only for translation
        calc = args[0]["calc"]        
        #ProbSolv = args[1][1]
        
        #fetches ros image
        img = roscv.rosImg2RGB(data)

        #calculates rotations
        if (calc == 0):
            img,ids,obsR,obsT = aruco.ArucoObservationMaker(img,K,D,self.markerIDoffset,self.Nmarkers,captureR=True,captureT=False)


            if  ids is not None and len(ids)>1:
                A =  probdefs.rotationProbDef(obsR,self.Nmarkers)

                self.ATA = self.ATA + np.dot(A.T,A) #way to save the matrix in a compact manner

        elif (calc == 1):
            
            img,ids,obsR,obsT = aruco.ArucoObservationMaker(img,K,D,self.markerIDoffset,self.Nmarkers,captureR=True,captureT=True)

            if  ids is not None and len(ids)>1:
                A,b =  probdefs.translationProbDef(obsT,R,self.Nmarkers)

                self.ATA = self.ATA + np.dot(A.T,A) #way to save the matrix in a compact manner

                self.ATb = self.ATb + np.dot(A.T,b) #way to save the matrix in a compact manner


            



        if(showVid == 1):
            cv2.imshow("Image window", img)
            cv2.waitKey(3)
        elif(showVid == 2):
            cv2.imshow("Image window", img)
            cv2.waitKey(0)