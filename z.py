import pickler2 as pickle
import visu
import json
import numpy as np

#ola = pickle.Pickle().Out("static/CamRot-NEW2camArucco_4.pickle")
ola = pickle.Pickle().Out("static/CameraInfo 20-04-2019.pickle")

ola['K'] = ola['K'].tolist()

lol = json.dumps(ola)

print(lol)

f = open("./static/camcalib_default.json",'w')
json.dump(ola,f)