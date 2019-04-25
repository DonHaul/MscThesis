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

    visu.ViewRefs(Rcam)

    #visu.ViewScene(R,t)

    R,t = synth.FakeArucoReal()

    #similar to output from ROS (I think)
    camsObs = synth.MultiCamSampleGeneratorFixed(Rcam,tcam,R,t)


    obsR, obsT = obsGen.GenerateCameraPairObs(camsObs,R,t)

    obsGen.ObservationViewer(obsR)
    #quit()

    B = probdefs.rotationProbDef(obsR,len(Rcam))  #95% confidence that it is correct


    C = np.dot(B.T,B) #C = B'B

    
    rotSols = algos.TotalLeastSquares(C,3,len(Rcam)) 

    print("global")
    visu.ViewRefs(rotSols)
    print("local")    
    rotSoles = mmnip.genRotRel(rotSols)    

    permuter = [[1,0,0],[0,0,-1],[0,1,0]]

    finalR=  mmnip.PermuteCols(rotSoles,permuter)

    visu.ViewRefs(finalR)



if __name__ == '__main__':
    main()