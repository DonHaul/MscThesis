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
    
    Rcam, tcam = synth.TestScene51()

    Raux = mmnip.genRotRelLeft(Rcam)
    
    visu.ViewRefs(Raux)

    R,t = synth.TiltedCams()

    #visu.ViewRefs(Rcam+R,tcam+t)

    #visu.ViewRefs(R)

    #similar to output from ROS (I think)
    camsObs = synth.MultiCamSampleGeneratorFixed(Rcam,tcam,R,t,noise=1)


    obsR, obsT = obsGen.GenerateCameraPairObs(camsObs,R,t)

    
    print(len(Rcam))
    B = probdefs.rotationProbDef(obsR,len(Rcam))  #95% confidence that it is correct


    C = np.dot(B.T,B) #C = B'B

    
    rotSols = algos.RProbSolv1(C,3,len(Rcam),canFlip=True) 
    #visu.ViewRefs(rotSols)

    #converts to world coordinates or into them
    rotSolsNotUsed = mmnip.Transposer(rotSols)
    #visu.ViewRefs(rotSolsNotUsed)

    #converts in first ref coordinates , 
    rr = mmnip.genRotRelLeft(rotSolsNotUsed)

    qrr=[]
    for r in rr:
        print(np.linalg.det(r))
        qrr.append(r.tolist())

    visu.ViewRefs(rr)


    #converts in first ref coordinates , 
    #rr = mmnip.genRotRelLeft(rotSols)
    #visu.ViewRefs(rr)

    print(rr)
    FileIO.putFileWithJson({'R':qrr},'R')





if __name__ == '__main__':
    main()