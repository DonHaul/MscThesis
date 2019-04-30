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
    camsObs = synth.MultiCamSampleGeneratorFixed(Rcam,tcam,R,t)


    obsR, obsT = obsGen.GenerateCameraPairObs(camsObs,R,t)

    

    B = probdefs.rotationProbDef(obsR,len(Rcam))  #95% confidence that it is correct


    C = np.dot(B.T,B) #C = B'B

    
    rotSols = algos.TotalLeastSquares(C,3,len(Rcam)) 

    print("global")
    visu.ViewRefs(rotSols)


    rotSoles = mmnip.genRotRel(rotSols)    

    print("local")
    visu.ViewRefs(rotSoles)

    permuter = [[0,1,0],[1,0,0],[0,0,1]]

    finalR=  mmnip.AxisSwapper(rotSoles,permuter)

    print("swapped")
    visu.ViewRefs(finalR)



if __name__ == '__main__':
    main()