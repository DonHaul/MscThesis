import numpy as np
import libs.errorCalcs
import libs.helperfuncs as thehelp
import numpy.matlib

lis=[]


lis.append({'ola':1,'p':0})
lis.append({'ola':2,'p':-1})
lis.append({'ola':3,'p':-2})

print(lis)

lis_you_want = [ item['ola'] for item in lis ]



print(lis_you_want)
print(type(lis_you_want))

quit()
n_observations=100

indexes=np.squeeze(np.indices((n_observations,)))

RR=[]
Rnorm=[]
R=np.zeros((3,3))

for i in range(n_observations):
    newR = np.random.rand(3,3)
    RR.append(newR)
    Rnorm.append(np.linalg.norm(newR,ord='fro'))
    R=R+ newR


realR = R / n_observations
print(realR)
realR_time = []
for i in range(n_observations):
    realR_time.append(realR)



print(libs.errorCalcs.MatrixListError(realR_time,RR))