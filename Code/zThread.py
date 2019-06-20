import threading
import cv2
import Queue as queue
import datetime
import time

import open3d

from libs import *


def worker(statev,stop):


    while(1==1):
        if(statev.nextIsAvailable):
            print("JERK5")
            statev.nextIsAvailable=False
            print(stop())
            if stop(): 
                break
                  
            




def Start(statev,stop):
    print("Starting Commandline")
    t1 = threading.Thread(target=worker,args=( statev,stop,))
    t1.start()