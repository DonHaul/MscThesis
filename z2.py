import numpy as np
import libs.errorCalcs
import libs.helperfuncs as thehelp
import numpy.matlib
import FileIO
import libs.helperfuncs as helperfuncs
import visu
import matmanip as mmnip

#Load aruco Model
arucoModel = FileIO.getJsonFromFile("./static/arucoModel 18-05-2019 01:27:54.json")['markers']


R=[]
t=[]

for marker in arucoModel:
    #get aruco model

    RR = np.asarray(marker['R'])
    tt = np.squeeze(np.asarray(marker['t']))

    R.append(RR)
    t.append(tt)

#R = helperfuncs.extractKeyFromDictList(arucoModel,'R')
#T = helperfuncs.extractKeyFromDictList(arucoModel,'t')


visu.ViewRefs(R,t,refSize=0.1)

newT = mmnip.Transl_fromWtoRef(R,t)

visu.ViewRefs(R,newT,refSize=0.1)

visu.ViewRefs(R+R,t+newT,refSize=0.1)

print(t)

print("WOWO K")
print(newT)

filepath =  FileIO.saveAsPickle("wowww",{'R':R,'T':newT})


#wowee = FileIO.getFromPickle(filepath)

print(wowee)