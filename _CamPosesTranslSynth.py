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

    visu.ViewRefs(Rcam,tcam)

    #visu.ViewScene(R,t)

    R,t = synth.FakeArucoReal()

    visu.ViewRefs(Rcam+R,tcam+t)

    #similar to output from ROS (I think)
    camsObs =synth.MultiCamSampleGeneratorFixed(Rcam,tcam,R,t)


    obsR, obsT = obsGen.GenerateCameraPairObs(camsObs,R,t)

    obsGen.ObservationViewer(obsR)
    #quit()

     # TRANSLATION STUFF
    A,b = probdefs.translationProbDef(obsT,Rcam,len(t))

    #x, res, rank, s = np.linalg.lstsq(A,b,rcond=None) #(A'A)^(-1) * A'b
    x= algos.LeastSquares(A,b)
    
    print("LS,LSnp,LSinv")

    x2 = np.dot(np.dot(np.linalg.pinv(np.dot(A.T,A)),A.T),b)

    print(np.sqrt(np.sum(x**2)))
    print(np.sqrt(np.sum(x2**2)))
    #print(x2)

    solsplit2 = np.split(x,len(t))
    visu.ViewRefs(Rcam,solsplit2)

    solt =[]
    #change t referential
    #for i in range(len(solsplit2)):
    #    solt.append(np.dot(-R[i].T,solsplit2[i]))























if __name__ == '__main__':
    main()