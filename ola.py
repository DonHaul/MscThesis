import pprint
import numpy as np
import Rtmat
import pickler as pickle
from synth import *

R1 = np.eye(3)
R2 = np.array([[0,1,0],[-1,0,0],[0,0,1]])


R=[]
R.append(R1)
R.append(R2)



ola0 = np.dot(R[0].T,np.array([10,10,0]))

ola = ola0 + [0,-20,0]

print(ola)


quit()


t=[]
t.append([0,0,0])
t.append([10,10,0])

ViewRefs(R,t)

r  = np.dot(R[0],R[1].T)
t0w=np.array([0,20,0])

ola = np.dot(r,t0w)

tw1 = ola + np.array([10,-10,0])

print(tw1)

