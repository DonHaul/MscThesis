
import numpy as np

from libs import *


#all variables that can change during the run should be here that are not local
class State(object):



    def __init__(self):
        self.imgStream={}
        self.ObservationMaker={}
        self.posescalculator={}

