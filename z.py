import open3d
import matmanip as mnip
import visu
import numpy as np
import pickler2 as pickle

import synth

Rww=mnip.genRotMat([0,0,0])
tww=[[0],[0],[0]]

#visu.ViewRefs([Rww,Rw1],)

Rw1=mnip.genRotMat([0,-90,0])
print(Rw1)
tw1=[[10],[0],[-10]]

tw = [[10],[0],[-10]]

totransform =  [[20],[0],[-10]]

a = np.dot(Rw1,totransform)+tw1
print(a)


#visu.ViewRefs([Rww,Rw1,mnip.genRotMat([0,-90,0])])

print(mnip.InvertT(Rw1,tw1))

#####

R,t = syn