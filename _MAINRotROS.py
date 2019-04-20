#HERE WILL BE the v1, but organized in a good fashion
import ArucoInfoGetter
import rospy
import algos
import pickler as pickle
from sensor_msgs.msg import Image

import cv2
import open3d
import numpy as np
import visu
import matmanip as mmnip


def main():

    ig = ArucoInfoGetter.ArucoInfoGetter()

    cameraName = "abretesesamo"

    rospy.init_node('my_name_is_jeff', anonymous=True)

    camInfo = pickle.Out("static/CameraInfo 20-04-2019.pickle")

     
    # all of the parameters
    cb_params =	{
    "showVideo": 1,
    "K": camInfo['K'],
    "D": camInfo['D'],
    "calc": 0 #0 is R 1 is t
}
     # all of the functions
    cb_functions = []



    rospy.Subscriber(cameraName+"/rgb/image_color", Image, ig.callback,(cb_params,cb_functions))


    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("shut")

    cv2.destroyAllWindows()
    
    rotsols = algos.TotalLeastSquares(ig.ATA,3,ig.Nmarkers)

    visu.ViewRefs(rotsols)
    
    Rrel = mmnip.genRotRel(rotsols)

    visu.ViewRefs(Rrel)


    #pickle.In("obs","RelMarkerRotations",Rrelations)
     

if __name__ == '__main__':
    main()