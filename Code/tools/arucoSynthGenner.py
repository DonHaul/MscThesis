import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+"/..")
from libs import *

R,t = synth.TestScene51()

visu.ViewRefs(R,t)

FileIO.saveAsPickle("TestScene_51",(R,t),path="./static/fakecangalhos/")