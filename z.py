import matmanip as mmnip
import numpy as np
import pickler as pickle
import visu


g = pickle.Out("pickles/ArucoRot.pickle")

#print("LOCALLL",g['Rglobal'])

#print("GLOBALL",g['Rlocal'])

permuter = [[0,-1,0],[-1,0,0],[0,0,-1]]

finalR=  mmnip.PermuteCols(g['Rlocal'],permuter)


pickle.In("ArucoRot","RlocalPermutated",finalR,putDate=False)


visu.ViewRefs(finalR)