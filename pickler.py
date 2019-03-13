import pickle

def In(name,data):
    f= open(name,"wb")
    pickle.dump(data,f)
    f.close

def Out(name):
    f= open(name,"rb")
    p  =  pickle.load(f)
    f.close

    return p
