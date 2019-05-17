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

p1 = algos.procrustesMatlab(mmnip.genRandRotMatrix(60),arg2,reflection='best')[2]['rotation']
p2 = algos.procrustesMatlab(mmnip.genRandRotMatrix(60),arg2,reflection=True)[2]['rotation']
p3 = algos.procrustesMatlab(mmnip.genRandRotMatrix(60),arg2,reflection=False)[2]['rotation']
p4 = algos.procrustesMatlabJanky(mmnip.genRandRotMatrix(60),np.eye(3))

#print("iaoww")


print("results")
print(p1)
print(p2)
print(p3)
print(p4)

print("DETERMINANTS")
d1 = np.linalg.det(p1)
d2 = np.linalg.det(p2)
d3 = np.linalg.det(p3)
d4 = np.linalg.det(p4)

print(d1)
print(d2)
print(d3)
print(d4)


#arg1 - R arg2
n1 = np.linalg.norm(arg1-np.dot(p1,arg2))
n2 = np.linalg.norm(arg1-np.dot(p2,arg2))
n3 = np.linalg.norm(arg1-np.dot(p3,arg2))
n4 = np.linalg.norm(arg1-np.dot(p4,arg2))

print("NORMS")
print(n1)
print(n2)
print(n3)
print(n4)
