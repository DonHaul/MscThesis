
import open3d
import matmanip as mnip
import visu
import numpy as np
import pickler2 as pickle

import synth



ola = pickle.Pickle().Out("pickles/wow 02-05-2019 01-07-33.pickle")

print(ola['sol'])

sols = ola['sol']

sols = np.flip(sols,axis=1)

solsplit = np.split(sols,12)  

#get actual rotation matrices by doing the procrustes
for sol in solsplit:
    print("opt1")

    dett = np.linalg.det(sol)
    print(np.linalg.det(sol))
    print(np.dot(sol.T,sol))

    #r,t=procrustes(np.eye(3),sol)

    #if(dett>0):
    #    print("TRANSPOSED IT")
    #    r=r.T


