import threading
import cv2
import Queue as queue
import datetime
import time
import state

def worker(statev):
    x=""
    count = 0
    while x!="q":
        x= raw_input("Enter command")
    
  
        val = x.split(" ")
        statev.stateDict = {val[0]:val[1]}
        
        print("state is:")
        print(statev.stateDict)

    return


def Start(statev):

    t1 = threading.Thread(target=worker,args=(statev,))
    t1.start()