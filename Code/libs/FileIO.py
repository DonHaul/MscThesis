import json
import numpy as np
import random
import datetime
import os
import open3d
import pickle
import pointclouder

saveInc=0

def savePCs(filename,pcs):
    '''
    saves a merged point cloud and also the separated pointclouds

    Args:
        filename String: what should the name be
        pcs [open3d.pointcloud]: list of all the retrieved pointclouds
    '''
    global saveInc
    saveInc=saveInc+1
    print(saveInc)
    print(filename)
    filename = filename+"_"+str(saveInc)

    pc = pointclouder.MergeClouds(pcs)

    #creates a file for the merged pointcloud
    open3d.write_point_cloud("./PC/"+filename+".ply", pc)

    #create a folder for the unmerged pointclouds
    try:
        os.mkdir("./PC/"+filename)
    except:
        print("PA")
    
    
    #save the individual pointclouds
    for i in range(len(pcs)):
        print(pcs[i])
        open3d.write_point_cloud("./PC/"+filename+"/pointcloud"+str(i)+".ply", pcs[i])




def getKDs(camNames):
    '''
    Gets Intrinsics and Distortion parameters.
    It locates the calibration files relative to the camera names passed

    Args:
        camNames [String]: list of all existing camera names
    '''
    K={}
    D={}


    for name in camNames:

        #fetches files
        filedict = getJsonFromFile("./static/camcalib_" + name +".json")

        #if file does not exist
        if(filedict==None):
            print("Calibration File Not Found")
            filedict = getJsonFromFile("./static/camcalib_default.json")

        k = np.asarray(filedict['K'], dtype=np.float32)

        #assigns parameters
        K[name]=k
        D[name]=np.asarray(filedict['D'], dtype=np.float32)

        intrinsic = {"K":K,"D":D}

    return intrinsic


def putFileWithJson(data,filename=None,folder=None):
    '''
    puts dictionary into a json

    Args:
        data: data to put in the file
        filename: name of the file
        folder: place to save the file to
    '''

    if folder is None:
        folder = "./tmp"
    
    if filename is None:
        filename = ""


    #assign an animal name to the file
    animalName = GetAnimalName()


    saveName = folder + "/" + filename+"_"+animalName + "_" +  datetime.datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
    f = open(saveName+".json","w")

    #save files
    json.dump(data,f)
    
    f.close()

    print("Saved File: "+str(saveName)+".json")

def GetAnimalName():
    '''
    Fetch animal name, from the names.json file
    '''
    f=open("static/names.json","r")

    arr = json.load(f)

    animalName = random.choice(arr)
    f.close()

    return animalName

def getFromPickle(filename):
    '''
    Gets data from pickle file

    Args:
        filename: name of the file to fetch the data from
    '''

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
    '''
    Get data from the json file

    Args:
        filename: path to the file to retrieve data from
    '''

    try:
        f=open(filename,"r")
    
        data = json.load(f)
        f.close()

        return data

    except IOError:
      print "Error: File does not appear to exist."
      return None

def LoadScene(filename):
    '''
    Gets R and T of a specific scene
    '''

    scene = getJsonFromFile(filename)


    R=[]
    t=[]
    camNames=[]
    for cam in  scene['cameras']:
        R.append(np.asarray(cam['R'], dtype=np.float32))
        t.append(np.asarray(cam['t'], dtype=np.float32))
        camNames.append(cam['name'])


    return R,t,camNames