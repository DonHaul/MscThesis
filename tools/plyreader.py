# examples/Python/Basic/pointcloud.py

import numpy as np
from open3d import *
import sys

def load_point_clouds(folder,voxel_size = 0.0):
    pcds = []
    for i in range(3):
        pcd = read_point_cloud(folder+"/pointcloud%d.ply" % i)
        #draw_geometries([pcd])
        
        pcds.append(pcd)
    return pcds

if __name__ == "__main__":

    print("Load a ply point cloud, print it, and render it")
    #pcd = read_point_cloud(sys.argv[1])
    #draw_geometries([pcd])

    if ".ply" in sys.argv[1]:
        pcd = read_point_cloud(sys.argv[1])
        draw_geometries([pcd])
    else:
        pcds = load_point_clouds(sys.argv[1])
        draw_geometries(pcds)

    
  

  