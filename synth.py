import open3d
import math
import numpy as np
import pickler as pickle
import pprint
import random
import Rtmat
import phase2_sparkle as phase2


def FetchKeyArray(key,dictlist):
    return [d[key] for d in dictlist]

def main():

    
    refs=[]

    R,t = FakeAruco()

    ViewRefs(R,t)

    groundTruths = Rtmat.genRotRel(R)
    
    #ViewRefs(groundTruths[0])

    

    
   
   

    obsR,obst = SampleGenerator(R,t,noise=1)
    
    #print(obst)

    B = phase2.problemDef(obsR,len(R))

    ola = np.dot(B.T,B)

    #checked seen here

    rotSols = phase2.TotalLeastSquares(ola,3,len(R))
    
    print("global")

    ViewRefs(rotSols)

    #very janky
    rotSoles = Rtmat.genRotRel(rotSols)
    print("local")
    ViewRefs(rotSoles[0])
    
 
    quit()
    
    print("YAOZA")

    



    rotS2 = []
    for r in rotSoles[0]:
        rotS2.append(np.dot(r,Rtmat.genRotMat([90,0,0])))
    ViewRefs(rotS2)

    rotS3 = []
    for r in rotS2:
        rotS3.append(np.dot(Rtmat.genRotMat([-90,0,0]),r))
    ViewRefs(rotS3)


        

    # TRANSLATION STUFF
    A,b = problemDef2(obst,rotS3,len(t))

    x, res, rank, s = np.linalg.lstsq(A,b,rcond=None) #(A'A)^(-1) * A'b


    #print(x,res,rank,s)    

    x2= np.dot( np.linalg.inv(np.dot(A.T,A)),np.dot(A.T,b)) #(A'A)^(-1) * A'b

    pprint.pprint(sum(np.square(np.dot(A,x)-b)) )
    pprint.pprint(sum(np.square(np.dot(A,x2)-b)))

    #JANKY
    solsplit2 = np.split(x,len(t))

    print(solsplit2[0].shape)


    ViewRefs(rotS3,solsplit2,refSize=1)

    #ViewRefs(None,[np.array([3,1,2]),np.array([3,1,1]),np.array([3,1,0])])

    

def problemDef2(observations,rotRel,N):

    #creates the left matrix in the problem formulation
    Ident = np.zeros((len(observations)*3,N*3))


    #creates the right matrix in the problem formulatin
    A = np.zeros((len(observations)*3,N*3))

    b = np.zeros((len(observations)*3,1))
            
    cnt = 0
    for obs in observations:
        #fills the matrices according to the observed pairs
        Ident[cnt*3:cnt*3+3,obs['to']*3:obs['to']*3+3]= np.eye(3)
        A[cnt*3:cnt*3+3,obs['from']*3:obs['from']*3+3]=  np.dot(rotRel[obs['to']],rotRel[obs['from']].T) #rotRel[obs['from']][obs['to']]

        #print(b[cnt*3:cnt*3+3,0])
        #print(obs['trans'])
        b[cnt*3:cnt*3+3,0:1]=obs['trans']

        cnt=cnt+1
    
    return Ident - A ,b




def SampleGenerator(R,t,samples=1000,noise = 0.00001,noiset=0.0001):

    
    r = np.zeros([len(R),1])

    while True:

        obsR = []
        obst = []

        for i in range(0,samples):

            #for each observation        

            #pick 2 different ids
            r1 =  random.randint(0, len(R)-1)
            r2 = r1
            while r2==r1:
                r2 = random.randint(0, len(R)-1)
            

            #t1w = (np.expand_dims(t[r1],0).T) # ref 1 no referencial do mundo
            #t2w = (np.expand_dims(t[r2],0).T) # ref 2 no referencial do mundo
            
            #tw2 = np.dot(-R[r2],t2w) # ref do mundo no referencial do 2
            #tw1 = np.dot(-R[r1],t1w) # ref do mundo no referencial do 1

            #t12=tw1 - np.dot(np.dot(R[r1],R[r2].T),tw2)
            print("#### # #### from "+ str(r1) + " to "+ str(r2))
          
            tw1 = np.dot(-R[r1].T,t[r1]) # <-- NAO ERA SUPOSTO TER O TRANSPOSTO WRONG / understand WHY
            #print(tw1)

            tw2 = np.dot(-R[r2].T,t[r2]) # <-- NAO ERA SUPOSTO TER O TRANSPOSTO WRONG / understand WHY
            #print(tw2)

            t21=tw1-np.dot(np.dot(R[r1],R[r2].T),tw2)
            print(t21)

            obsR.append({"from":r2,"to":r1,"rot":np.dot(Rtmat.genRotMat(np.squeeze([np.random.rand(3,1)*noise])),np.dot(R[r1],R[r2].T))})
            obst.append({"from":r2,"to":r1,"trans":t21}) #Aqui as translacoes geradas a bit WRONG sao desacopladas, no entanto na realidade estao sempre dependentes das rotacoes

            raw_input("press key...")
            r[r1]=1
            r[r2]=1

        #print(sum(r))
        #there is at least one observation per marker
        if sum(r)==len(R):
            break

    return obsR,obst
    
def draw_geometry(pcd):
    # The following code achieves the same effect as:
    # draw_geometries([pcd])
    vis = open3d.Visualizer()

    vis.create_window(width=800 ,height=600)
    opt = vis.get_render_option()
    opt.background_color = np.asarray([0, 0, 0])
    for geo in pcd:
        vis.add_geometry(geo)
    vis.run()
    vis.destroy_window()


def ViewRefs(R=None,t=None,refSize=10, w=None,h=None):

    #in case one of them is none, get the one that is not zero
    N = len(R) if R is not None else len(t)

    refs = []

    if t is None:
        t = []
        for i in range(0,N):
            t.append([i*20,0,0]) 



    if R is None:
        R = []
        for i in range(0,N):
            print(R)
            R.append(Rtmat.genRotMat([0,0,0])) 


   

    for i in range(N):

        P=np.eye(4)

        
        P[0:3,0:3]= R[i]
        P[0:3,3]=np.squeeze(t[i])

        refe = open3d.create_mesh_coordinate_frame(refSize, origin = [0, 0, 0])
        refe.transform(P)

        refs.append(refe)

    draw_geometry(refs)

    return refs



def GenReferential(angle,t):

    refe = open3d.create_mesh_coordinate_frame(size = 10, origin = [0, 0, 0])
    
    refe.transform(P)

    return refe


def TotalLeastSquaresT(C,Nleast,split):
    '''
    ola
    '''

    u,s,vh = np.linalg.svd(C)
    
    solution = u[:,-Nleast:]

    #split in 3x3 matrices, dat are close to the rotation matrices but not quite
    rotsols = []
    solsplit = np.split(solution,split)

    return solsplit
    
def FakeAruco():

    R=[]
    t=[]

    R.append(Rtmat.genRotMat([0,0,0]))
    #R.append(Rtmat.genRotMat([0,0,0]))
    #R.append(Rtmat.genRotMat([0,0,0]))

    R.append(Rtmat.genRotMat([0,90,0]))
    #R.append(Rtmat.genRotMat([0,90,0]))
    #R.append(Rtmat.genRotMat([0,90,0]))
    
    R.append(Rtmat.genRotMat([0,180,0]))
    #R.append(Rtmat.genRotMat([0,180,0]))
    #R.append(Rtmat.genRotMat([0,180,0]))

    R.append(Rtmat.genRotMat([0,270,0]))
    #R.append(Rtmat.genRotMat([0,270,0]))
    #R.append(Rtmat.genRotMat([0,270,0]))
    
    t.append(np.array([0,0,10]))
    #t.append(np.array([0,-20,10]))
    #t.append(np.array([0,20,10]))

    t.append(np.array([10,0,0]))
    #t.append(np.array([10,-20,0]))
    #t.append(np.array([10,20,0]))

    t.append(np.array([0,0,-10]))
    #t.append(np.array([0,-20,-10]))
    #t.append(np.array([0,20,-10]))

    t.append(np.array([-10,0,0]))
    #t.append(np.array([-10,-20,0]))
    #t.append(np.array([-10,20,0]))

    return R,t






if __name__ == '__main__':
    main()
