import open3d
import matmanip as mnip
import visu
import numpy as np
import pickler2 as pickle


Rww=mnip.genRotMat([0,0,0])
tww=[[0],[0],[0]]


Rw1=mnip.genRotMat([0,90,0])
tw1=[[10],[0],[10]]

visu.ViewRefs([Rww,Rw1],[tww,tw1])

print(mnip.Transform(tww,Rw1,[[10],[0],[-10]]))