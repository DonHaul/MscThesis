import json
import numpy as np
import FileIO
import visu
import algos
import matmanip as mmnip
import open3d

a = np.array([[1],[2],[3]])

b = np.array([4])
print(b.shape)
c = np.array([[1]])

print(np.squeeze(a))

print(np.squeeze(b))

lol =(np.squeeze(c))

print(lol)
print(type(lol))

lol = lol.tolist()
if(type(lol)==int):
    print("wow")

print(len(lol))

