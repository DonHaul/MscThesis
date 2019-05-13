import threading
import cv2
import Queue as queue
import datetime
import time
import state
import visu
import open3d

def worker(statev,rospy):
    x=""
    count = 0
    while x!="q":
        x= raw_input("Enter command")
        if "pc" in x:
            visu.draw_geometry([statev.pc])
            #print("wow")
            
        elif "R" in x:
            print("calculating R")
            statev.CalcRthenStartT()
        elif "T" in x:
            print("calculating t")
            statev.CalcT()
            rospy.signal_shutdown('Quit')
            break
        else:
            print("invalid command")

    return


def Start(statev,rospy):

    t1 = threading.Thread(target=worker,args=(statev,rospy,))
    t1.start()