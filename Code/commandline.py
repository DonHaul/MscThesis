import threading
import cv2
import Queue as queue
import datetime
import time

import open3d

from libs import *


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
                
                open3d.draw_geometries(scene)
                visu.draw_geometry(scene)   
            else:
                time.sleep(int(ola[1]))
                visu.draw_geometry([statev.pc])

            print("PATH TO SAVE IS")
            print(statev.PCPath)
            FileIO.savePCs(statev.PCPath,statev.pcs,statev.pc)
            
        elif "lol" in x:
            print("2 cams calc")
            statev.CalcRT2()
            rospy.signal_shutdown('Quit')
            break
        elif "setcam" in x:

            ola = x.split(" ")
            statev.curCam=int(ola[1])
            print("Current cammera changed to:"+str(statev.curCam))
        elif "-" in x:

            ola = x.split(" ")
            if len(ola)>1:
                for i in range(3):
                    print(i)
                    time.sleep(1)
                print("*SNAPPING*")
                statev.snapcount=int(ola[1])
            else:
                statev.snapcount=1
            
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