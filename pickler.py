import pickle
import datetime

_curTime = datetime.datetime.now()

_pickledata = {} #should be global, but it still works with magic


def ShowData():
    print("DATA IS:",_pickledata)



def In(name,key,data,path="pickles/",putDate=True):

    _pickledata[key]=data
    
    saveName = path+name

    if putDate:
        saveName = saveName+" " + _curTime.strftime("%d-%m-%Y %H-%M-%S")

    f= open(saveName+".pickle","wb")
    

    pickle.dump(_pickledata,f)
    f.close
    print("Data Saved on: " + name+_curTime.strftime("%d-%m-%Y %H-%M-%S")+".pickle")


def Out(name):
    f= open(name,"rb")
    p  =  pickle.load(f)
    f.close

    #whenever reading a pickle, it imports variables to _pickledata
    for key, value in p.iteritems():
        _pickledata[key] = value
     
    return p
