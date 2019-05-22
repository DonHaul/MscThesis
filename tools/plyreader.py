# examples/Python/Basic/pointcloud.py

import numpy as np
from open3d import *
import sys

if __name__ == "__main__":

    print("Load a ply point cloud, print it, and render it")
    pcd = read_point_cloud(sys.argv[1])
    print(pcd)
    print(np.asarray(pcd.points))
    draw_geometries([pcd])

    quit()

    print("Downsample the point cloud with a voxel of 0.05")
    downpcd = voxel_down_sample(pcd, voxel_size = 0.05)
    draw_geometries([downpcd])

    print("Recompute the normal of the downsampled point cloud")
    estimate_normals(downpcd, search_param = KDTreeSearchParamHybrid(
            radius = 0.1, max_nn = 30))
    draw_geometries([downpcd])

    print("Print a normal vector of the 0th point")
    print(downpcd.normals[0])
    print("Print the normal vectors of the first 10 points")
    print(np.asarray(downpcd.normals)[:10,:])
    print("")

  