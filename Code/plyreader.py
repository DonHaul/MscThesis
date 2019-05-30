# examples/Python/Basic/pointcloud.py

import numpy as np
from open3d import *
import sys

def load_point_clouds(folder):
    pcds = []
    for i in range(3):
        pcd = read_point_cloud(folder+"/pointcloud%d.ply" % i)
        #draw_geometries([pcd])
        
        pcds.append(pcd)
    return pcds


    
  

  