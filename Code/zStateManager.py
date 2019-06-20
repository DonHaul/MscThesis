
import numpy as np

from libs import *


#all variables that can change during the run should be here that are not local
class State(object):

    def __init__(self):

        self.data={}
        self.nextIsAvailable=False

    def next(self):

        print("HEYY")

        return self.data      
