"""
probdefs.py

This module contains loads in or saves out variables that we may want to monitor
"""

import pickle
import datetime

#Date the script was ran
_curTime = datetime.datetime.now()

#should be global, but it still works with magic
_pickledata = {} 


def ShowData():
    '''Show all data currently to be saved'''
    print("DATA IS:",_pickledata)



def In(name,key,data,path="pickles/",putDate=True):
    '''Saves a dictionary with things out into a pickle file

    Args:
        name (str):Filename
        key (str):Name of the variable will be saved as
        data (anything): Data to be saved in the dict
        path (str): Where will it be saved
        putData (bool,optional): whether or not the current data is concatenated to the file name
    '''

    _pickledata[key]=data #gets data into internal variable, this lets it so other variables dont overwrite the file after
    
    saveName = path+name #path and filename

    #add date
    if putDate:
        saveName = saveName+" " + _curTime.strftime("%d-%m-%Y %H-%M-%S")
    
    f= open(saveName+".pickle","wb")    #open file and write bytes
    
    pickle.dump(_pickledata,f)          #dump stuff into that file
    
    f.close

    print("Data Saved on: " + name+_curTime.strftime("%d-%m-%Y %H-%M-%S")+".pickle")


def Out(name):
    '''Loads the dictionary out of the file

    Args:
        name (str): path and filen to load
    
    Returns:
        p (dict):dictionary with that file's information
    '''
    f= open(name,"rb")
    p  =  pickle.load(f)
    f.close

    #whenever reading a pickle, it imports variables to _pickledata
    for key, value in p.iteritems():
        _pickledata[key] = value
     
    return p
