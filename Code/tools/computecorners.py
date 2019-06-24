import sys
from libs import *
import numpy as np
import open3d


def main(argv):

        #Load aruco Model
    arucoModel = FileIO.getFromPickle(argv[0])
    arucoData = FileIO.getJsonFromFile(argv[1])

    arucoData['idmap'] = aruco.markerIdMapper(arucoData['ids'])



    R = arucoModel['R']
    T = arucoModel['T']
    


    print(arucoModel)
    print(arucoData)

    allcorners= np.zeros((len(arucoData['ids']*4),3))

    allpositions = visu.ViewRefs(R,T,refSize=0.1,view=False)

    count = 0
    for i in arucoData['ids']:

        aa = aruco.Get3DCorners(i,arucoData,arucoModel)
        aa = np.asarray(aa)
        print("SHAPES")
        print(count*4,count*4+4)
        print(aa.shape) 
        print(allcorners[count*4:count*4+4,:].shape)
        allcorners[count*4:count*4+4,:]=aa
        count = count + 1
    

    for i in range(allcorners.shape[0]):

        mesh_sphere=open3d.create_mesh_sphere(radius = 0.003)
        mesh_sphere.paint_uniform_color([0.8, 0.8, 0])
        mesh_sphere.transform(mmnip.Rt2Homo(np.eye(3),np.squeeze(allcorners[i,:])))
        allpositions.append(mesh_sphere)

        

        count=count+1

    visu.draw_geometry(allpositions)
    
    FileIO.saveAsPickle("corners",allcorners,putDate=True)





if __name__ == '__main__':
    main(sys.argv[1:])