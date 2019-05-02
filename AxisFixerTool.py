import open3d
import matmanip as mnip
import visu
import numpy as np
import pickler2 as pickle
import matmanip as mmnip

curPickle = pickle.Pickle()

refsUnchanged = curPickle.Out("pickles/CamRot 01-05-2019 16-41-47.pickle")

loc = refsUnchanged['Rloc']

print(loc)

visu.ViewRefs(loc)

newRefs = mmnip.AxisSwapper(loc,[[0,1,0],[1,0,0],[0,0,1]])

visu.ViewRefs(newRefs)

print("Check if determinant is 1 and RTR=Identity")
for r in newRefs:
    print(np.linalg.det(r))
    print(np.dot(r.T,r))

savePickle = pickle.Pickle()
savePickle.In("CamRot-NEW2camArucco_4","R",newRefs,putDate=False)