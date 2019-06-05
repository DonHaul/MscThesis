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



mat1=np.random.random((3,10))

RR = mmnip.genRotMat([-70,20,45])
TT = np.array([69.69,-10.211,-10])
print(RR,TT)

mat2=mmnip.Transform(mat1,RR.T,TT)
#mat1 = mmnip.genRandRotMatrix(40)
#mat2 = np.eye(3)

results=[]

print("WOWZA")
print(mat1.shape)
R,T  = algos.PointCrustes(mat1.T,mat2.T)
print(R,T)
R,T = algos.procrustesMatlabJanky2(mat2.T,mat1.T)
print(R,T)
quit()



