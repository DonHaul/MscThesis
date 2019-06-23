import threading
import cv2
import Queue as queue
import datetime
import time

import open3d

from libs import *

import rospy

def worker(statev,stop):

    x=""

    while True:

        x= raw_input("Enter command")
        if "R" in x:
            print("HELP I HAVE DA BIG GAY")
            statev.posescalculator.CalcRthenStartT()

        elif "T" in x:
            statev.posescalculator.CalcT()
            
            rospy.signal_shutdown("Successful T")
            statev.stop_threads=True
        else:
            print("invalid command")

        if stop():
            break




def Start(statev,stop):
    print("Starting Commandline")
    t1 = threading.Thread(target=worker,args=(statev,stop,))
    t1.start()