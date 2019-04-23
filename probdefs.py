import numpy as np


def rotationProbDef(observations,N):

    #creates the left matrix in the problem formulation
    Ident = np.zeros((len(observations)*3,N*3))


    #creates the right matrix in the problem formulatin
    A = np.zeros((len(observations)*3,N*3))
            
    cnt = 0
    for obs in observations:
        #fills the matrices according to the observed pairs

        if obs['to'] > 12 or obs['from'] > 12:
            print("skippity: weird index found")
            continue

        
        Ident[cnt*3:cnt*3+3,obs['to']*3:obs['to']*3+3]= np.eye(3)
        A[cnt*3:cnt*3+3,obs['from']*3:obs['from']*3+3]= obs['R']

        
        #print(obs)
        #print("Ident")
        #print(Ident[cnt*3:cnt*3+3,:])
        #print("A")
        #print(A[cnt*3:cnt*3+3,:])
        #raw_input("Press Enter to continue...")
        
        cnt=cnt+1
    return Ident - A

def rotationProbDefv2(observations,N):

    #creates the left matrix in the problem formulation
    Ident = np.zeros((len(observations)*3,N*3))


    #creates the right matrix in the problem formulatin
    A = np.zeros((len(observations)*3,N*3))
            
    cnt = 0
    for obs in observations:
        #fills the matrices according to the observed pairs
        Ident[cnt*3:cnt*3+3,obs['from']*3:obs['from']*3+3]= np.eye(3)
        A[cnt*3:cnt*3+3,obs['to']*3:obs['to']*3+3]= obs['R'].T

        
        #print(obs)
        #print("Ident")
        #print(Ident[cnt*3:cnt*3+3,:])
        #print("A")
        #print(A[cnt*3:cnt*3+3,:])
        #raw_input("Press Enter to continue...")
        
        cnt=cnt+1
    return Ident - A

def rotationProbDefv3(observations,N):

    #creates the left matrix in the problem formulation
    Ident = np.zeros((N*3,len(observations)*3))


    #creates the right matrix in the problem formulatin
    A = np.zeros((N*3,len(observations)*3))
            
    cnt = 0
    for obs in observations:
        #fills the matrices according to the observed pairs
        Ident[obs['from']*3:obs['from']*3+3,cnt*3:cnt*3+3]= np.eye(3)
        A[obs['to']*3:obs['to']*3+3,cnt*3:cnt*3+3]= obs['R']

        
        #print(obs)
        #print("Ident")
        #print(Ident[cnt*3:cnt*3+3,:])
        #print("A")
        #print(A[cnt*3:cnt*3+3,:])
        #raw_input("Press Enter to continue...")
        
        cnt=cnt+1
    return Ident - A

def translationProbDef(observations,rotRel,N):
    '''
    observations - observations fecthed from the camera or synthetic
    rotRel - rotatios relative to the world
    N - number of markers
    '''

    #creates the left matrix in the problem formulation
    Ident = np.zeros((len(observations)*3,N*3))


    #creates the right matrix in the problem formulatin
    A = np.zeros((len(observations)*3,N*3))

    b = np.zeros((len(observations)*3,1))
            
    cnt = 0
    for obs in observations:


        if obs['to'] > 12 or obs['from'] > 12:
            print("skippity: weird index found")
            continue


        Ident[cnt*3:cnt*3+3,obs['to']*3:obs['to']*3+3]= np.eye(3)
        A[cnt*3:cnt*3+3,obs['from']*3:obs['from']*3+3]=  np.eye(3) #rotRel[obs['from']][obs['to']]

        
        b[cnt*3:cnt*3+3,0]=-np.dot( rotRel[obs['to']],obs['t'])

        cnt=cnt+1
    
    return Ident - A ,b
