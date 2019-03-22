import pickle
import datetime

curTime = datetime.datetime.now()

def In(name,data):

  

    f= open("pickles/"+name+curTime.strftime("%d-%m-%Y %H-%M-%S")+".pickle","wb")
    

    pickle.dump(data,f)
    f.close

def Out(name):
    f= open(name,"rb")
    p  =  pickle.load(f)
    f.close



    return p
