import json
import numpy as np
import random
import datetime
import os
import open3d
import pickle
import pointclouder

def savePCs(filename,pcs):


    pc = pointclouder.MergeClouds(pcs)

    print("./PC/"+filename+".ply")

    open3d.write_point_cloud("./PC/"+filename+".ply", pc)

    try:
        os.mkdir("./PC/"+filename)
    except:
        print("PA")
    
    
    for i in range(len(pcs)):
        print(pcs[i])
        open3d.write_point_cloud("./PC/"+filename+"/pointcloud"+str(i)+".ply", pcs[i])




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

def GetAnimalName():
    f=open("static/names.json","r")

    arr = json.load(f)

    animalName = random.choice(arr)
    f.close()

    return animalName

def getFromPickle(filename):

    p={}

    try:
        f= open(filename,"rb")
        p  =  pickle.load(f)
        f.close
    except IOError:
        print("ERROR: No Such File")

        
    return p


def saveAsPickle(name,data,path="pickles/",putDate=True,animal=True):
    '''
        Args:
        name (str):Filename
        key (str):Name of the variable will be saved as
        data (anything): Data to be saved in the dict
        path (str): Where will it be saved
        putData (bool,optional): whether or not the current data is concatenated to the file name
    '''

    saveName = path+name #path and filename

    if(animal):
        saveName = saveName+"_"+GetAnimalName()

    #add date
    if putDate:
        saveName = saveName+"_" + datetime.datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
    
    f= open(saveName+".pickle","wb")    #open file and write bytes
    
    pickle.dump(data,f)          #dump stuff into that file
    
    f.close

    print("Data Saved on: " + saveName +".pickle")


    return saveName + ".pickle"


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