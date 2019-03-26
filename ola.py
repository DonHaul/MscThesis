import numpy as np
import open3d
import pickler as pickle
import procrustes as proc
import open3d


ola = pickle.Out("pickles/obs26-03-2019 12-02-35.pickle")

C=ola["AtA"]
Nmarkers=12

u, s, vh = np.linalg.svd(C)
#print("Eigenfs")
#print(u.shape, s.shape, vh.shape)

solution = u[:,-3:]

#split in 3x3 matrices, dat are close to the rotation matrices but not quite
rotsols = []
solsplit = np.split(solution,Nmarkers)

#get actual rotation matrices by doing the procrustes
for sol in solsplit:
    r,t=proc.procrustes(np.eye(3),sol)
    rotsols.append(r)



rref = rotsols[0]

frames =[]
counter = 0
#make ref 1 the reference and display rotations
for r in rotsols:

    #r=np.dot(rref,r.T)
    #r=np.dot(r,rref.T)
    refe = open3d.create_mesh_coordinate_frame(size = 0.6, origin = [0, 0, 0])

    trans = np.zeros((4,4))
    trans[3,3]=1
    trans[0,3]=counter #linha ,coluna
    trans[0:3,0:3]=r#np.eye(3)

    refe.transform(trans)
    frames.append(refe)

    counter = counter +1


open3d.draw_geometries(frames)

#print(ig.Nmarkers + ig.markerIDoffset)
Rrelations = [[] for i in range(Nmarkers)] #correct way to make 2d list

#generate R between each things
for i in range(0,Nmarkers):
    for j in range(0,Nmarkers):
        Rrelations[i].append(np.dot(rotsols[j],rotsols[i].T))
        #print(i,j)
        #print(np.dot(rotsols[j],rotsols[i].T))
    
    #print(i)
    #print(len(Rrelations[i]))
