import rosinterface as roscv
import numpy as np
import cv2



class ArucoInfoGetter(object):
    def __init__(self):
      
        self.count = 0
        self.Nmarkers = 12 #number of markers, MUST BE CONTIGUOUS for this to work
        self.markerIDoffset=-2 #offset dos markers, como vao do 2 ao 12, o offset e 2

        self.C = np.zeros((self.Nmarkers *3,self.Nmarkers *3))

        self.mats = {}




    def callback(self,data,args):

        showVid = args[0]["showVideo"]
        K=args[0]["K"]
        D=args[0]["D"]
        ArucoObservationMaker = args[1][0]
        ProbSolv = args[1][1]
        LSFit = args[1][2]

        

        img = roscv.rosImg2RGB(data)


        img,ids = ArucoObservationMaker(img,K,D,self.markerIDoffset,self.Nmarkers)


        if  ids is not None and len(ids)>1:
            A,b = ProbSolv(observations,R,self.Nmarkers)

            self.mats["A"] = self.mats["A"] + np.dot(A.T,A) #way to save the matrix in a compact manner
            self.mats["b"] = self.mats["b"] + np.dot(A.T,b)


            



        if(showVid == 1):
            cv2.imshow("Image window", img)
            cv2.waitKey(3)
        elif(showVid == 2):
            cv2.imshow("Image window", img)
            cv2.waitKey(0)