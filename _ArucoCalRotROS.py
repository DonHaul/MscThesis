#HERE WILL BE the v1, but organized in a good fashion
import ArucoInfoGetter
import rospy
import algos
import pickler2 as pickle
from sensor_msgs.msg import Image

import cv2
import open3d
import numpy as np
import visu
import matmanip as mmnip

import probdefs

#import snapper

def main():
    showVideo = 1
    calc = 0  #0 is R 1 is t

    

    cameraName = "abretesesamo"

    rospy.init_node('my_name_is_jeff', anonymous=True)

    camInfo = pickle.Pickle().Out("static/CameraInfo 20-04-2019.pickle")


    ig = ArucoInfoGetter.ArucoInfoGetter(camInfo['K'],camInfo['D'],showVideo,calc)
     
    #snapper.Start(ig.GetImg)

    # all of the parameters
    cb_params =	{}
     # all of the functions
    cb_functions = []

    

    rospy.Subscriber(cameraName+"/rgb/image_color", Image, ig.callback,(cb_params,cb_functions))


    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("shut")

    cv2.destroyAllWindows()
    



    print("global1")
    


    #B = probdefs.rotationProbDef(obsR,len(R))  #95% confidence that it is correct

    #C = np.dot(B.T,B) #C = B'B

    print("global1")
    

    rotSols = algos.RProbSolv1(ig.ATA,3,ig.Nmarkers)  
    visu.ViewRefs(rotSols)

    #converts to world coordinates or into them
    rotSolsNotUsed = mmnip.Transposer(rotSols)
    visu.ViewRefs(rotSolsNotUsed)

    #converts in first ref coordinates , 
    #rr = mmnip.genRotRelRight(rotSols)
    #visu.ViewRefs(rr)


    #converts in first ref coordinates , 
    rr = mmnip.genRotRelLeft(rotSols)
    visu.ViewRefs(rr)
    
    pickle.Pickle().In("ROTTARUCOv2","R",rr)

if __name__ == '__main__':
    main()