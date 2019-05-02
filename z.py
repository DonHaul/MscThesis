import pickler2 as pickle
import visu

#ola = pickle.Pickle().Out("static/CamRot-NEW2camArucco_4.pickle")
ola = pickle.Pickle().Out("pickles/CamRot 02-05-2019 03-36-35.pickle")
print(ola)

visu.ViewRefs(ola['R'])