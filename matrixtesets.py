
import numpy as np


A=np.array([[1,2,3],[4,5,6],[7,8,9]])

print(A)

b = A[:,-1]

print(b)

b= b*-1


print(b)


A[:,-1] = b

print(A)