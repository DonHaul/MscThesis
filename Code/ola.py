from libs import *
import numpy as np
import pprint


def procrustesV7(X, Y):


    n,m = X.shape
    ny,my = Y.shape

    muX = X.mean(0)
    muY = Y.mean(0)

    X0 = X - muX
    Y0 = Y - muY

    # optimum rotation matrix of Y
    A = np.dot(X0.T, Y0)
    
    U,s,Vt = np.linalg.svd(A,full_matrices=False)
    V = Vt.T
    T = np.dot(V, U.T)

    c = muX - np.dot(muY, T)


    return T,c

def showShapes(wa,mat1,mat2):
    for w in wa:
        print("MM")
        minn = np.dot(w,mat1)-mat2
        
        print(minn.shape)
        mm = np.linalg.norm(minn)
        print(mm)

        minn = np.dot(w.T,mat1)-mat2
        mm = np.linalg.norm(minn)
        print(mm)

        minn = np.dot(w,mat2)-mat1
        mm = np.linalg.norm(minn)
        print(mm)

        minn = np.dot(w.T,mat2)-mat1
        mm = np.linalg.norm(minn)
        print(mm)
        

def procsNEW(X,Y):

    n,m = X.shape
    ny,my = Y.shape

    print(X.shape)

    #MAKE SURE THIS VALUE IS 3
    muX = np.expand_dims(X.mean(1), axis=1) 
    muY = np.expand_dims(Y.mean(1), axis=1) 
    print(X)
    print("WOO")
    print(muX)

    X0 = X - muX
    Y0 = Y - muY  

    print(X0)

        # optimum rotation matrix of Y
    A = np.dot(Y0, X0.T)
    
    print(A)

    U,s,Vt = np.linalg.svd(A,full_matrices=False) 

    print("R is")
    R = np.dot(Vt.T,U.T)
    print(R)

    t = muX - np.dot(R,muY)

    return R,t

mat1=np.random.random((3,10))
mat2=np.random.random((3,10))

#mat1 = mmnip.genRandRotMatrix(40)
#mat2 = np.eye(3)

procsNEW(mat1,mat2)
quit()
results=[]

results.append(algos.procrustesMatlab(mat1,mat2,reflection='best')[2]['rotation'])
results.append(algos.procrustesMatlab(mat1,mat2,reflection='best')[2]['rotation'])
results.append(algos.procrustesMatlab(mat1,mat2,reflection=True)[2]['rotation'])
results.append(algos.procrustesMatlab(mat1,mat2,reflection=False)[2]['rotation'])
results.append(procrustesV7(mat1,mat2)[0])


results.append(res1)
results.append(res2)
results.append(res3)


pprint.pprint(results)

showShapes(results,mat1,mat2)


