import os
from distutils.dir_util import copy_tree
import libs

ola = os.listdir('./Logs')


for o in ola:
    
    newO =  o.replace(":", "|")

    if newO == o:
        continue
    
    libs.FileIO.CreateFolder('./Logs/' + newO,putDate=False)
    copy_tree('./Logs/' + o ,'./Logs/' + newO)
