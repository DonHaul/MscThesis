import json
import numpy as np
import FileIO
import visu


arucoModel = FileIO.getJsonFromFile("./scenes/emu 13-05-2019 20:17:32.json")

R=[]
t=[]

for marker in arucoModel['cameras']:
    #get aruco model

    RR = np.asarray(marker['R'])
    tt = np.squeeze(np.asarray(marker['t']))

    print(tt)

    R.append(RR)
    t.append(tt)

    R.append(np.eye(3))
    t.append([0,0,0])

visu.ViewRefs(R,t,refSize=0.1)


