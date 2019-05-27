import numpy as np
import libs.errorCalcs
import libs.helperfuncs as thehelp
import numpy.matlib
import FileIO
import libs.helperfuncs as helperfuncs
import visu
import matmanip as mmnip
import algos


p = algos.procrustesMatlabJanky2(mmnip.genRandRotMatrix(3),mmnip.genRandRotMatrix(3))

print(p)