import pickle
import datetime

curTime = datetime.datetime.now()

pickledata = {}


def In(name,key,data,path="pickles/",putDate=True):

    pickledata[key]=data

    saveName = path+name

    if putDate:
        saveName = saveName+" " + curTime.strftime("%d-%m-%Y %H-%M-%S")

    f= open(saveName+".pickle","wb")
    

    pickle.dump(pickledata,f)
    f.close
    print("Data Saved on: " + name+curTime.strftime("%d-%m-%Y %H-%M-%S")+".pickle")

'''
def In(name,key,data,path="./pickles/",putDate=True):

    pickledata[key]=data

    saveName = path+name+" "
    if putDate:
        saveName = saveName + curTime.strftime("%d-%m-%Y %H-%M-%S")

    saveName = saveName +".pickle"

    f= open(saveName)
    

    pickle.dump(pickledata,f)
    f.close
    print("Data Saved on: " + name+curTime.strftime("%d-%m-%Y %H-%M-%S")+".pickle")
'''


def Out(name):
    f= open(name,"rb")
    pickledata  =  pickle.load(f)
    f.close


     
    return pickledata
