import matmanip as mmnip
import numpy as np
import pickler as pickle
import visu
import random


a = pickle.Out("static/ArucoModel 23-04-2019 13-45-37.pickle")

visu.ViewRefs(a['R'],a['t'],refSize=0.1)