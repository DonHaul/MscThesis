import json
import numpy as np
import random
import datetime

def getKDs(camNames):
    K={}
    D={}

    for name in camNames:
        filedict = getJsonFromFile("./static/camcalib_" + name +".json")

        #if file does not exist
        if(filedict==None):
            print("Calibration File Not Found")
            filedict = getJsonFromFile("./static/camcalib_default.json")

        k = np.asarray(filedict['K'], dtype=np.float32)

        
        K[name]=k
        D[name]=np.asarray(filedict['D'], dtype=np.float32)

        intrinsic = {"K":K,"D":D}

    return intrinsic


def putFileWithJson(data,filename=None,folder=None):

    if folder is None:
        folder = "./tmp"
    
    if filename is None:
        filename = ""

    f=open("static/names.json","r")

    arr = json.load(f)

    animalName = random.choice(arr)
    f.close()

    saveName = folder + "/" + filename+"_"+animalName + "_" +  datetime.datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
    f = open(saveName+".json","w")

    json.dump(data,f)
    
    f.close()

    print("Saved File: "+str(saveName)+".json")


def getJsonFromFile(filename):

    try:
        f=open(filename,"r")
    
        data = json.load(f)
        f.close()

        return data

    except IOError:
      print "Error: File does not appear to exist."
      return None

def LoadScene(filename):

    scene = getJsonFromFile(filename)


    R=[]
    t=[]
    camNames=[]
    for cam in  scene['cameras']:
        R.append(np.asarray(cam['R'], dtype=np.float32))
        t.append(np.asarray(cam['t'], dtype=np.float32))
        camNames.append(cam['name'])


    return R,t,camNames