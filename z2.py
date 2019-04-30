# examples/Python/Basic/working_with_numpy.py

import copy
import numpy as np
from open3d import *

if __name__ == "__main__":

    # generate some neat n times 3 matrix using a variant of sync function
    x = np.linspace(-3, 3, 401)
    mesh_x, mesh_y = np.meshgrid(x,x)
    z = np.sinc((np.power(mesh_x,2)+np.power(mesh_y,2)))
    z_norm = (z-z.min())/(z.max()-z.min())
    xyz = np.zeros((np.size(mesh_x),3))
    xyz[:,0] = np.reshape(mesh_x,-1)
    xyz[:,1] = np.reshape(mesh_y,-1)
    xyz[:,2] = np.reshape(z_norm,-1)
    print('xyz')
    print(xyz)

    # Pass xyz to Open3D.PointCloud and visualize
    pcd = PointCloud()
    pcd.points = Vector3dVector(xyz)
    print(xyz.shape)
    print(type(xyz[0][0]))
    draw_geometries([pcd])