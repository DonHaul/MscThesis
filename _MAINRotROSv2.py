#HERE WILL BE the v1, but organized in a good fashion
import ArucoInfoGetter
import rospy
def main():

    ig = ArucoInfoGetter.ArucoInfoGetter()

    cameraName = "abretesesamo"

    rospy.init_node('my_name_is_jeff', anonymous=True)

    camInfo = pickle.Out("static/CameraInfo 20-04-2019.pickle")

     
    # all of the parameters
    cb_params =	{
    "showVideo": 1,
    "K": camInfo['K'],
    "D": camInfo['D']
}
     # all of the functions
    cb_functions = [ArucoObservationMaker,probdefs.translationProbDef,algos.LeastSquares]



    rospy.Subscriber(cameraName+"/rgb/image_color", Image, ig.callback,(cb_params,cb_functions))


    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("shut")

    cv2.destroyAllWindows()

    pickle.In("obs","AtA",ig.C)

    
    rotsols = algos.TotalLeastSquares(ig.C,3,ig.Nmarkers)
    

    
    
    rref = rotsols[0].T

    frames =[]
    counter = 0
    #make ref 1 the reference and display rotations
    for r in rotsols:

        #r=np.dot(rref,r.T)
        refe = open3d.create_mesh_coordinate_frame(size = 0.6, origin = [0, 0, 0])

        trans = np.zeros((4,4))
        trans[3,3]=1
        trans[0,3]=counter #linha ,coluna
        trans[0:3,0:3]=r

        refe.transform(trans)
        frames.append(refe)

        counter = counter +1

    
    open3d.draw_geometries(frames)

    
    Rrel = mmnip.genRotRel(rotsols)
    
    '''
    for i in range(0,ig.Nmarkers):
        for j in range(0,ig.Nmarkers):
            print("Ok:",(i,j))
            print(Rrelations[j][i])
    '''

    pickle.In("obs","RelMarkerRotations",Rrelations)
     

if __name__ == '__main__':
    main()