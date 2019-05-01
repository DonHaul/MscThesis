import open3d
import matmanip as mnip
import visu
import numpy as np
import pickler2 as pickle

arucoModel = pickle.Pickle().Out("static/ArucoModel 01-05-2019 15-38-20.pickle")

visu.ViewRefs(arucoModel['R'],arucoModel['t'],refSize=0.1)