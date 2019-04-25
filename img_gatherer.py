import rosinterface as roscv
import numpy as np
import cv2
import aruco
import probdefs



class img_gather(object):
    def __init__(self,N_cams):
      
        self.N_cams = N_cams

        self.images =  np.zeros((480,640*N_cams,3),dtype=np.uint8)

        
    def showImg(self):
        cv2.imshow("Image window ",self.images)           
        cv2.waitKey(10)

    def GatherImg(self,camId,img):
        #print("on gather img")
        self.images[0:480,camId*640:camId*640+640,0:3]=img
        
        #print(np.sum(img-self.images[0:480,camId*640:camId*640+640,0:3]))
        
        




   