import open3d
import matmanip as mnip
import visu
import numpy as np
import pickler2 as pickle

import synth



R,t = synth.Scenev1()

visu.ViewRefs(R,t)

print("Riw")
for r in R:
    print(r)


print("tiw")
for r in t:
    print(r)

newR=[]
newt = []

ref =1

newR = mnip.genRotRelLeft(R,ref)

for i in range(0,len(t)):
    newt.append(np.dot(R[ref].T,t[i])+mnip.InvertT(R[ref],t[ref]))


visu.ViewRefs(newR,newt)
