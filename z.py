import open3d
import matmanip as mnip
import visu
import numpy as np

R0 = mnip.genRotMat([0,0,0])

R1 = mnip.genRotMat([0,90,0])
print(R0)
print(R1)
visu.ViewRefs([R0,R1])

visu.ViewRefs([R0,R1,np.dot(R1,R0.T)])