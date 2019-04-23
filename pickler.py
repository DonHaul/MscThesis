import pickle
import datetime

curTime = datetime.datetime.now()

pickledata = {} #should be global, but it still works with magic


def ShowData():
    print("DATA IS:",pickledata)



def In(name,key,data,path="pickles/",putDate=True):

    pickledata[key]=data
    
    saveName = path+name

    if putDate:
        saveName = saveName+" " + curTime.strftime("%d-%m-%Y %H-%M-%S")

    f= open(saveName+".pickle","wb")
    

    pickle.dump(pickledata,f)
    f.close
    print("Data Saved on: " + name+curTime.strftime("%d-%m-%Y %H-%M-%S")+".pickle")


def Out(name):
    f= open(name,"rb")
    p  =  pickle.load(f)
    f.close

    #whenever reading a pickle, it imports variables to pickledata
    for key, value in p.iteritems():
        pickledata[key] = value
     
    return p
