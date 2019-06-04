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
        
        minn = np.dot(w,mat2)-mat1        
        print(minn.shape)
        mm = np.linalg.norm(minn)
        print(mm)


def RotCrustes(Mat1,Mat2):
        '''
        Problem that it solves is
        ||R Mat1 - Mat2||^2
        '''
        return orthogonal_procrustes(Mat1.T,Mat2.T)[0]

def PointCrustes(mtx1,mtx2):

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
mat2 = np.eye(3)

results=[]

R,T  = PointCrustes(mat1.T,mat2.T)
results.append(R)
results.append(orthogonal_procrustes(mat1.T,mat2.T)[0])
showShapes(results,mat1,mat2)

results.append(RotCrustes(mat1,mat2))
print("MATTS")
print(RotCrustes(mat1,mat2))
print(mat1)
print(mat2)
print(T)
#mmnip.isRotation([RR])

visu.ViewRefs([RR]+results)


