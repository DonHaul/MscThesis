import json
import numpy as np

R=[]

R.append(np.random.rand(3,3))
R.append(np.random.rand(3,3))
R.append(np.random.rand(3,3))

t=[]

t.append(np.random.rand(3,))
t.append(np.random.rand(3,))
t.append(np.random.rand(3,))

print(R)
print(t)

cameras=[]

for RR,tt in zip(R,t):
    print(tt,RR)

    cameras.append({"R":RR.tolist(),"t":tt.tolist()})


print(cameras)

f = open("lol.json","w")

json.dump(cameras,f)

f.close()