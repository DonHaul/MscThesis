from libs import *
import numpy as np
import pprint
from scipy.linalg import orthogonal_procrustes
from scipy.spatial import procrustes



def showShapes(wa,mat1,mat2):
    for w in wa:
        print("MM")
        print(np.linalg.det(w))
        print(w.shape)
        
        minn = np.dot(mat2.T,w.T)-mat1.T        
        print(minn.shape)
        mm = np.linalg.norm(minn)
        print(mm)

        print(mm)


def procsNEW(mtx1,mtx2):

    # translate all the data to the origin
    mtx1t =mtx1 - np.mean(mtx1, 0)
    mtx2t =mtx2 - np.mean(mtx2, 0)

    norm1 = np.linalg.norm(mtx1t)
    norm2 = np.linalg.norm(mtx2t)

    if norm1 == 0 or norm2 == 0:
        raise ValueError("Input matrices must contain >1 unique points")

    # change scaling of data (in rows) such that trace(mtx*mtx') = 1
    mtx1t /= norm1
    mtx2t /= norm2

    # transform mtx2 to minimize disparity
    R, s = orthogonal_procrustes(mtx1t, mtx2t)
    mtx2t = np.dot(mtx2t, R.T) * s

    t = np.mean(mtx2, 0)-np.dot(R,np.mean(mtx1, 0))


    return R,t

mat1=np.random.random((3,10))

RR = mmnip.genRotMat([32,13120,2190])
TT = np.array([69,-10,-2910])

mat2=mmnip.Transform(mat1,RR.T,TT)
#mat1 = mmnip.genRandRotMatrix(40)
#mat2 = np.eye(3)

#print("Mats are")
#print(mat1,mat2)
#print(mat1.shape,mat2.shape)


results=[]

R,T  = procsNEW(mat1.T,mat2.T)


showShapes(results,mat1,mat2)

print(T)
#mmnip.isRotation([RR])

visu.ViewRefs([RR,R])


