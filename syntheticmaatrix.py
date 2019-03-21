import open3d
import math
import numpy as np

#console.log("mat rot")



#def makeRx():
theta=15
#math.cos(theta)

n_referentials = 3


def genRotMat(angle):

    Rx = [[1,0,0],[0,math.cos(angle[0]),-math.sin(angle[0])],[0,math.sin(angle[0]),math.cos(angle[0])]]

    Ry = [[math.cos(angle[1]),0,math.sin(angle[1])],[0,1,0],[-math.sin(angle[1]),0,math.cos(angle[1])]]


    Rz = [[math.cos(angle[2]),-math.sin(angle[2]),0],[math.sin(angle[2]),math.cos(angle[2]),0],[0,0,1]] 

    aux = np.dot(Rx,Ry)


    return np.dot(aux,Rz)


#print(np.dot(rot.T,rot))

#print(np.linalg.det(rot))

rot=[]
#generate matrices
for i in range(0,n_referentials):


    rot.append(genRotMat(np.random.rand(3,1)))


print(len(rot))

rotrel=[[1,2,3],[1,2,3],[0,0,0]]

print(rotrel)

#generate measurements
for i in range(0,n_referentials):
    for j in range(0,n_referentials):

        rotrel[i][j]=np.dot(rot[i].T,rot[j])

        print("===========")
        print((i,j))
        print(rotrel[i][j])


#add noise
std = 0.0001


for i in range(0,n_referentials):
    for j in range(0,n_referentials):

        noise  =  std * np.random.randn(3,3)

        rotrel[i][j]= rotrel[i][j] + noise

        print("===========")
        print((i,j))
        print(rotrel[i][j])



solv = np.zeros([n_referentials*3,n_referentials*3])



def changeMat(solv,change,x,y):
    print(x*3+0,x*3+3,y*3+0,y*3+3)
    solv[x*3+0:x*3+3,y*3+0:y*3+3] = change
    return solv

solv = changeMat(solv,np.eye(3),0,0)
solv = changeMat(solv,rotrel[1][2],1,2)
solv = changeMat(solv,rotrel[2][1],2,1)


print("===========")
print(solv)

print("===========")
w,v = np.linalg.eig(solv)


print(w)
print(v)