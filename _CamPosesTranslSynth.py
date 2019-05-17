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

    R,t = synth.FakeAruco()
    
    Rcam, tcam = synth.TiltedCams()

    Rcam = mmnip.genRotRelLeft(Rcam)

    visu.ViewRefs(Rcam+R,tcam+t)

    Rcam = FileIO.getJsonFromFile("./tmp/R boar 17-05-2019 00:25:21.json")['R']

    Rcam = np.asarray(Rcam)

    Rcam = np.split(Rcam,3,axis=0)
    
    RR = []

    for r in Rcam:
        RR.append(np.squeeze(r))

    print(RR)
    #pprint.pprint(t)

    Rcam=RR

    visu.ViewRefs(Rcam+R,tcam+t)

    print(Rcam[0].T)
    print(type(Rcam[0]))

    visu.ViewRefs(Rcam,tcam)

    #visu.ViewScene(R,t)

    

    #Rcam = mmnip.genRotRel(Rcam)

    
   

    

    #similar to output from ROS (I think)
    camsObs =synth.MultiCamSampleGeneratorFixed(Rcam,tcam,R,t)

    #print(camsObs)
    #print("ahdioad")

    obsR, obsT = obsGen.GenerateCameraPairObs(camsObs,R,t)

    #print(obsT)

    #obsGen.ObsViewer(obsR)
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