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

import FileIO



def main():

    #mesh = read_triangle_mesh("models/filmCamera.ply")
    #mesh.compute_vertex_normals()
    #mesh.paint_uniform_color([1, 0.706, 0])
    #draw_geometries([mesh])

    R,t = synth.TiltedCams()
    
    Rcam, tcam = synth.TestScene51()

    #Rcam = mmnip.genRotRelLeft(Rcam)

    visu.ViewRefs(Rcam,tcam,showRef=True)

    Rcam1 = FileIO.getJsonFromFile("./tmp/R stingray 18-05-2019 02:58:26.json")['R']

    Rcam1 = np.asarray(Rcam1)

    Rcam1 = np.split(Rcam1,4,axis=0)
    
    RR = []

    for r in Rcam1:
        RR.append(np.squeeze(r))

    print(RR)
    #pprint.pprint(t)

    Rcam1=RR

    #visu.ViewRefs(Rcam+R,tcam+t)

    #similar to output from ROS (I think)
    camsObs =synth.MultiCamSampleGeneratorFixed(Rcam,tcam,R,t)

    obsR, obsT = obsGen.GenerateCameraPairObs(camsObs,R,t)

  

    # TRANSLATION STUFF
    A,b = probdefs.translationProbDef(obsT,Rcam1,len(Rcam1))

    #x, res, rank, s = np.linalg.lstsq(A,b,rcond=None) #(A'A)^(-1) * A'b
    x= algos.LeastSquares(A,b)
    
    print("LS,LSnp,LSinv")

    x2 = np.dot(np.dot(np.linalg.pinv(np.dot(A.T,A)),A.T),b)

    print(np.sqrt(np.sum(x**2)))
    print(np.sqrt(np.sum(x2**2)))
    #print(x2)

    solsplit2 = np.split(x,len(Rcam1))
    visu.ViewRefs(Rcam1,solsplit2,showRef=True)

    solt =[]
    #change t referential
    #for i in range(len(solsplit2)):
    #    solt.append(np.dot(-R[i].T,solsplit2[i]))























if __name__ == '__main__':
    main()