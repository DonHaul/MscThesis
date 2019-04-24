import numpy as np
import matmanip as mmnip


def ObservationViewer(observations,what='R'):
    for obs in observations:
        print("from:"+str(obs['from'])+" to:"+str(obs['to']))
        print(obs[what])

def SampleGenMultiCam(camObs1,camObs2):
    pass

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
            for obsiR in camsObs[i]:
                #and through all the obs of the other
                for obsjR in camsObs[j]:
                



                    #confusing as fuck i, know
                    # pretty much we have Rcam_i -> obsId_i and Rcam_j -> obsId_j   - to what each camera is observating is alwaying
                    # 'ObsId' = 'to' , and the cameraId on the array is the 'from'
                    obsR.append({"from":i,"to":j,"R": np.linalg.multi_dot([obsiR['R'].T,R[obsiR['obsId']],R[obsjR['obsId']].T,obsjR['R']])})


                    
                    #AND MATCHERU THEM

                    #confusing as fuck i, know
                    # pretty much we have Rcam_i -> obsId_i and Rcam_j -> obsId_j   - to what each camera is observating is alwaying
                    # 'ObsId' = 'to' , and the cameraId on the array is the 'from'
                    Rbetweenaruco = np.dot(R[obsiR['obsId']],R[obsjR['obsId']].T)
                    tbetweenaruco = np.dot(R[obsiR['obsId']].T, t[obsjR['obsId']] - t[obsjR['obsId']])

                    new_t =  mmnip.Transform(obsiR['t'],Rbetweenaruco,tbetweenaruco)
                    tij = mmnip.InverseTransform(new_t,obsjR['R'],obsjR['t'])

                    obsT.append({"from":i,"to":j,"t": tij})

    print(str(len(obsR))+ " Rotation Observations Were Generated") # should be same as Ncameras_C_2 * Nobs^2
    print(str(len(obsT))+ " Translation Observations Were Generated") 

    return obsR,obsT