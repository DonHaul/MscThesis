import pickler as pickle
import procrustes as proc
import numpy as np




def procrustes(X,Y):
    muX = X.mean(0)
    muY = Y.mean(0)

    X0 = X - muX
    Y0 = Y - muY

    # optimum rotation matrix of Y
    H = np.dot(X0.T, Y0)
    U,s,Vt = np.linalg.svd(H)
    V = Vt.T
    R = np.dot(V, U.T)
    print("usVt",U,s,Vt)
    t = muX - np.dot(muY, R)


    return R, t




disdata = pickle.Out("data.pickle")

P1= disdata['P1']
P2= disdata['P2']

_,_,proctf = proc.procrustes(P1,P2,scaling=False,reflection=False)   

print("matlab",proctf)

R,t = procrustes(P1,P2)

print("R,T",(R,t))
