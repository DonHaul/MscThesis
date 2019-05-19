import threading
import cv2
import Queue as queue
import datetime
import time

import visu
import open3d

def worker(statev,rospy):
    x=""
    count = 0
    while x!="q":
        x= raw_input("Enter command")
        if "pc" in x:
            
            #print("wow")
            ola = x.split(" ")
            if(len(ola)==1):
                scene = visu.ViewRefs(statev.camPoses[0],statev.camPoses[1],view=False,refSize=1)
                scene.append(statev.pc)
                visu.draw_geometry(scene)   
            else:
                time.sleep(int(ola[1]))
                visu.draw_geometry([statev.pc])
        elif "lol" in x:
            print("2 cams calc")
            statev.CalcRT2()
            rospy.signal_shutdown('Quit')
            break
        elif "-" in x:
            #for i in range(3):
            #    print(i)
            #    time.sleep(1)
            print("*SNAP*")
            statev.readyToCapture=True


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
    print("Starting Commandline")
    t1 = threading.Thread(target=worker,args=(statev,rospy,))
    t1.start()