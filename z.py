import matmanip as mmnip
import numpy as np
import pickler as pickle
import visu
import random


#a = pickle.Out("static/ArucoModel 23-04-2019 13-45-37.pickle")

#visu.ViewRefs(a['R'],a['t'],refSize=0.1)

noise=1

lol = np.squeeze([np.random.rand(3,1)*noise-np.ones((3,1))*noise/2])

print(lol)

haha  = mmnip.genRotMat(lol)

print(haha)

print(np.linalg.det(haha))