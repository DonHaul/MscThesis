import pickle
import datetime

curTime = datetime.datetime.now()

pickledata = {}

def In(name,key,data,path="pickles/",encoding="wb"):

    pickledata[key]=data

    f= open(path+name+" "+curTime.strftime("%d-%m-%Y %H-%M-%S")+".pickle",encoding)
    

    pickle.dump(pickledata,f)
    f.close
    print("Data Saved on: " + name+curTime.strftime("%d-%m-%Y %H-%M-%S")+".pickle")

def Out(name):
    f= open(name,"rb")
    p  =  pickle.load(f)
    f.close



    return p
