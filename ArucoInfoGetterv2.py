import rosinterface as roscv
import numpy as np
import cv2
import aruco
import probdefs



class ArucoInfoGetter(object):
    def __init__(self,K,D,showVid=0,calc=0,R=None,camId=0,gather=None):
      
        self.count = 0
        self.Nmarkers = 12 #number of markers, MUST BE CONTIGUOUS for this to work
        self.markerIDoffset=-2 #offset dos markers, como vao do 2 ao 12, o offset e 2

        self.ATA = np.zeros((self.Nmarkers *3,self.Nmarkers *3)) #*3 because rotations matrix is 3x3

        self.ATb = np.zeros((self.Nmarkers *3,1)) # *3 because tranlations are 3x1

        #intrinsic Params
        self.K = K
        #Distortion params
        self.D = D
        #show video
        self.showVid = showVid
        #translation
        self.calc = calc

        self.R = R

        self.camId = camId

        self.gather = gather

        


    def callback(self,data,args):

        #print("calc")
        #print(self.calc)
        camId=0

        #if self.calc>2:
            #print("camId")
            #print(self.camId)

        #fetches ros image
        img = roscv.rosImg2RGB(data)
        #print(img.shape)
        #calculates rotations
        if (self.calc == 0):
            img,ids,obsR,obsT = aruco.ArucoObservationMaker(img,self.K,self.D,self.markerIDoffset,self.Nmarkers,captureR=True,captureT=False)


            if  ids is not None and len(ids)>1:
                A =  probdefs.rotationProbDef(obsR,self.Nmarkers)

                self.ATA = self.ATA + np.dot(A.T,A) #way to save the matrix in a compact manner

        elif (self.calc == 1):
            
            img,ids,obsR,obsT = aruco.ArucoObservationMaker(img,self.K,self.D,self.markerIDoffset,self.Nmarkers,captureR=True,captureT=True)
            
            if  ids is not None and len(ids)>1:
                A,b =  probdefs.translationProbDef(obsT,self.R,self.Nmarkers)

                self.ATA = self.ATA + np.dot(A.T,A) #way to save the matrix in a compact manner

                self.ATb = self.ATb + np.dot(A.T,b) #way to save the matrix in a compact manner

                #self.obstList =self.obstList + obsT

        self.gather.GatherImg(self.camId,img)
        

        if(self.showVid == 1 and self.camId==0):
            
            
            self.gather.showImg()
            #print(img.shape)
             
            #cv2.imshow("Image window "+str(self.camId) , img)           
            #cv2.waitKey(3)
        #elif(self.showVid == 2):
        #    cv2.imshow("Image window "+str(self.camId), img)
        #    cv2.waitKey(0)