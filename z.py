import json
import numpy as np
import FileIO
import visu
import algos
import matmanip as mmnip

arg1 = mmnip.genRandRotMatrix(60)
arg2 = np.eye(3)
print("arg1 is")
print(arg1)
print(np.linalg.det(arg1))
p1 = algos.procrustes3(arg1.T,arg2.T,fixReflection=False)[0]
p2 = algos.procrustesMatlab(arg1,arg2,reflection=False)[2]['rotation']
p7  = algos.procrustes3(arg1,arg2,fixReflection=False)[0]


#print("iaoww")


print("results")
print(p1.T)
print(p2)
print(p7)

print("DETERMINANTS")
d1 = np.linalg.det(p1)
d2 = np.linalg.det(p2)
d7 = np.linalg.det(p7)
print(d1)
print(d2)
print(d7)


#arg1 - R arg2
n1 = np.linalg.norm(arg1-np.dot(p1.T,arg2))
n2 = np.linalg.norm(arg1-np.dot(p2,arg2))
n7 = np.linalg.norm(arg1-np.dot(p7,arg2))

print("NORMS")
print(n1)
print(n2)
print(n7)
