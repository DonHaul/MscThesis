import open3d
from open3d import *
import numpy as np
import copy
import synth

import matmanip as mmnip

import visu 

import random

import probdefs
import algos

import observationgenner as obsGen


def main():

    #mesh = read_triangle_mesh("models/filmCamera.ply")
    #mesh.compute_vertex_normals()
    #mesh.paint_uniform_color([1, 0.706, 0])
    #draw_geometries([mesh])
    
    Rcam, tcam = synth.Scenev1()

    

    #visu.ViewScene(R,t)

    R,t = synth.FakeAruco()

    visu.ViewRefs(Rcam+R,tcam+t)

    #similar to output from ROS (I think)
    camsObs = synth.MultiCamSampleGeneratorFixed(Rcam,tcam,R,t,noise=1)


    obsR, obsT = obsGen.GenerateCameraPairObs(camsObs,R,t)

    
    print(len(Rcam))
    B = probdefs.rotationProbDef(obsR,len(Rcam))  #95% confidence that it is correct


    C = np.dot(B.T,B) #C = B'B

    
    rotSols = algos.RProbSolv1(C,3,len(Rcam)) 

  
    visu.ViewRefs(rotSols)

    print("global2")
    #rotSols = algos.RProbSolv1(C,3,len(R))    
    #visu.ViewRefs(rotSols)
     
    
    print("local1")
    
    rr = mmnip.genRotRel(rotSols)
    visu.ViewRefs(rr)
    
    print("localleft1")
    rr = mmnip.globalRotateRotsl(rotSols)
    visu.ViewRefs(rr)

    print("localweird mode")

    Rrelations = []

    #generate R between each things
    for j in range(0,len(rotSols)):
        Rrelations.append(np.dot(rotSols[j].T,rotSols[0])) #Rw2*R1w' = R12

    
    visu.ViewRefs(Rrelations)




if __name__ == '__main__':
    main()