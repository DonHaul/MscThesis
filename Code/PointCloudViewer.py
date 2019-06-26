"""
PosePipelineMaker.py

Generates and executes a pipeline to estimate poses
"""


import numpy as np
import time
import rospy
import numpy as np
from shutil import copyfile
from libs import *
import sys
import threading

import PointCloudVisualizer

import Classes.State as State

import CommandLine
from open3d import *

def worker(state):

    #boom = create_mesh_sphere(10)
    #print(type(boom))
    vis = Visualizer()
    vis.create_window()
    vis.run()
            
    #vis.add_geometry(state.pcs[0])

    #print("EEERRRRR")
    #print(state.pcs)
    
    



    count = 0

    
    while state.stop_threads==False:
        time.sleep(1)
        print(state.updated)
        if(state.updated==True):


            count=count+1
            print("UPDATE THEINGS",count)
            state.updated=False
            #print(state.pcs)


            #print(state.xyz)
            #print(state.rgb)
            #pc = pointclouder.Points2Cloud(state.xyz,state.rgb)
            vis.add_geometry(state.pcs[0])
            vis.update_geometry()
            vis.poll_events()
            vis.update_renderer()
            #print(pc)
            #visu.draw_geometry([state.pcs[0]])
            

            

        

            



def main(argv):

    poses = FileIO.getFromPickle(argv[0]+"/poses.pickle")

    state = State.State()
    
    print(poses)

    print("YEET")

    PointCloudVisualizer.PCViewer(poses,argv[0],(480,640),state)


    #sets thread for pipeline
    t1 = threading.Thread(target=worker,args=( state,))
    t1.start()
    
    

    try:
        print("SPINN")
        rospy.spin()
    except KeyboardInterrupt:
        print("shut")

    state.Stop()
    
    t1.join()

    
if __name__ == '__main__':
    main(sys.argv[1:])