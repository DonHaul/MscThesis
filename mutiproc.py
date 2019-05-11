import multiprocessing 
import visu
import globalthings
import rosinterface
import time
import numpy as np
  
def print_cube(num): 
    """ 
    function to print cube of given num 
    """
    print("Cube: {}".format(num * num * num)) 
  
def print_square(num): 
    """ 
    function to print square of given num 
    """
    print("Square: {}".format(num * num)) 
  

def wow(conn,lock):

    camsName=["abretesesamo"]

    try:
        count=0
        while True:
            #get clouds here
            pcs_frame=[]
            for i in range(0,len(camsName)):

    
                pc,_,_ = rosinterface.GetPointCloudRGBD(camsName[i],globalthings.camInfo['K'])

                
                conn.send({'points':np.asarray(pc.points),'colors':np.asarray(pc.colors)})
                
                count = count + 1
                #lock.release()

                #time.sleep()
    

            #visu.draw_geometry([pc])
            #if save_image:
            # vis.capture_screen_image("temp_%04d.jpg" % i)

            #time.sleep(1)
    except KeyboardInterrupt:
        print('interrupted!')
        conn.close()
    

    #vis.destroy_window()

   


if __name__ == "__main__": 

    lock = multiprocessing.Lock()

    # creating processes 
    conn1, conn2 = multiprocessing.Pipe()
    p1 = multiprocessing.Process(target=wow, args=(conn1,lock,)) 
    p2 = multiprocessing.Process(target=visu.draw_non_blocking_thread, args=(conn2,lock,)) 
  
    # starting process 1 
    p1.start() 
    # starting process 2 
    p2.start() 
  
    # wait until process 1 is finished 
    p1.join() 
    # wait until process 2 is finished 
    p2.join() 
  
    # both processes finished 
    print("Done!") 


