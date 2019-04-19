import pprint
import numpy as np
import Rtmat
import pickler as pickle


A = np.array([[1,2],[3,4],[5,6]])

pinv = (np.linalg.pinv(A))

print(pinv)

mypinv = np.dot(np.linalg.inv(np.dot(A.T,A)),A.T)

print(mypinv)
