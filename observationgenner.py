import numpy as np
import matmanip as mmnip


def ObservationViewer(observations,what='R'):
    for obs in observations:
        print("from:"+str(obs['from'])+" to:"+str(obs['to']))
        print(obs[what])

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
            for k in range(0,len(camsObs[i]['obsR'])):
                #and through all the obs of the other
                for l in range(0,len(camsObs[j]['obsR'])):

                    
                    #AND MATCHERU THEM

                    #confusing as fuck i, know
                    # pretty much we have Rcam_i -> obsId_i and Rcam_j -> obsId_j   - to what each camera is observating is alwaying
                    # 'ObsId' = 'to' , and the cameraId on the array is the 'from'
                    obsR.append({"from":i,"to":j,"R": np.linalg.multi_dot([camsObs[i]['obsR'][k]['R'].T,R[camsObs[i]['obsR'][k]['obsId']],R[camsObs[j]['obsR'][l]['obsId']].T,camsObs[j]['obsR'][l]['R']])})

                    #AND MATCHERU THEM

                    #confusing as fuck i, know
                    # pretty much we have Rcam_i -> obsId_i and Rcam_j -> obsId_j   - to what each camera is observating is alwaying
                    # 'ObsId' = 'to' , and the cameraId on the array is the 'from'
                    Rbetweenaruco = np.dot(R[camsObs[i]['obsR'][k]['obsId']],R[camsObs[j]['obsR'][l]['obsId']].T)
                    tbetweenaruco = np.dot(R[camsObs[i]['obsR'][k]['obsId']].T, t[camsObs[j]['obsR'][l]['obsId']] - t[camsObs[j]['obsR'][l]['obsId']])

                    new_t =  mmnip.Transform(camsObs[i]['obsT'][k]['t'],Rbetweenaruco,tbetweenaruco)
                    tij = mmnip.InverseTransform(new_t,camsObs[j]['obsR'][l]['R'],camsObs[j]['obsT'][l]['t'])

                    obsT.append({"from":i,"to":j,"t": tij})

    print(str(len(obsR))+ " Rotation Observations Were Generated") # should be same as Ncameras_C_2 * Nobs^2
    print(str(len(obsT))+ " Translation Observations Were Generated") 

    return obsR,obsT