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
    camsObs = MultiCamSampleGeneratorStatic(Rcam,tcam,R,t)

    obsR, obsT = GenerateCameraPairObs(camsObs,R,t)

    ObservationViewer(obsR)
    #quit()

    B = probdefs.rotationProbDef(obsR,len(Rcam))  #95% confidence that it is correct


    C = np.dot(B.T,B) #C = B'B

    print(C.shape)

    rotSols = algos.TotalLeastSquares(C,3,len(Rcam)) 

    print("global")
    visu.ViewRefs(rotSols)
    print("local")    
    rotSoles = mmnip.genRotRel(rotSols)    

    permuter = [[1,0,0],[0,0,-1],[0,1,0]]

    finalR=  mmnip.PermuteCols(rotSoles,permuter)

    visu.ViewRefs(finalR)



#attention this does not check if all cameras have matches
def MultiCamSampleGeneratorStatic(Rcam,tcam,R,t):
    '''
    simulates one single frame in every camera and matches results
    '''
    nObs = 5 #number of observations of a camera in a certain frame

    camsObs = []

    noise = 0.01
    
    #generate SingleCam Samples
    for i in range(0,len(Rcam)):
        
        #pick random ones
        rnds = random.sample(range(1, len(R)), nObs)

        obsR=[]
        obsT=[]

        for r in rnds:
            
            #generate the samples
            obsR.append({"obsId":r,"R": np.dot(mmnip.genRotMat(np.squeeze([np.random.rand(3,1)*noise])), np.dot(R[r],Rcam[i].T))}) 
            #obsT

        #assign them to each camera
        camsObs.append({"obsR":obsR,"obsT":obsT})

    
    
    return camsObs

def GenerateCameraPairObs(camsObs,R,t):
    '''
    R and t are from aruco
    '''

    obsR = []
    obsT = []
    #this double for loop makes all camera combinations

    #between one camera
    for i in range(0,len(camsObs)):
        #and another camera
        for j in range(i+1,len(camsObs)):
            
            #this double loop matches every possible observation in each camera

            #go through all the obs of one camera
            for obsiR in camsObs[i]['obsR']:
                #and through all the obs of the other
                for obsjR in camsObs[j]['obsR']:
                
                    #AND MATCHERU THEM

                    #confusing as fuck i, know
                    # pretty much we have Rcam_i -> obsId_i and Rcam_j -> obsId_j   - to what each camera is observating is alwaying
                    # 'ObsId' = 'to' , and the cameraId on the array is the 'from'
                    obsR.append({"from":i,"to":j,"R": np.linalg.multi_dot([obsiR['R'].T,R[obsiR['obsId']],R[obsjR['obsId']].T,obsjR['R']])})

    print(str(len(obsR))+ " Observations Were Generated") # should be same as Ncameras_C_2 * Nobs^2

    return obsR,obsT

def ObservationViewer(observations,what='R'):
    for obs in observations:
        print("from:"+str(obs['from'])+" to:"+str(obs['to']))
        print(obs[what])

#R": np.linalg.multi_dot([camsObs[j]['R'].T,R[camsObs[j]['obsId']],R[camsObs[i]['obsId']].T,camsObs[i]['R'].T])})


















if __name__ == '__main__':
    main()