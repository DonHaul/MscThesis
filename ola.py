import pprint
import numpy as np
import Rtmat
import pickler as pickle

d = pickle.Out("pickles/TLS01-04-2019 20-28-02.pickle")

haa  =  np.random.rand(5,5)



a = np.dot(haa.T,haa)

#a= d['C']

pprint.pprint(a)


print(Rtmat.CheckSymmetric(a))

u,s,vh = np.linalg.svd(a)

#print("matu")
#pprint.pprint(u)

#print("matvh")
#pprint.pprint(vh)

print("Howequal",abs(u-vh.T).max())


