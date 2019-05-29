import open3d
import numpy as np

def Points2Cloud(points,rgb=None):
    '''
    Converts 3D points and colors into a pointcoud
    '''

    #make point cloud    
    cloud = open3d.PointCloud()

    cloud.points = open3d.Vector3dVector(points)

    if(rgb is not None):

        permuter=np.array([[0,0,1],[0,1,0],[1,0,0]])

        rgb = np.dot(rgb,permuter)
        cloud.colors = open3d.Vector3dVector(rgb/255.0) #range is 0-1 hence the division
        
    return cloud

def MergeClouds(clouds):
    '''
    Merge clouds into a single cloud
    '''

    mergedCloud = open3d.PointCloud()

    xyz=np.empty((0,3))
    rgb=np.empty((0,3))

    for cloud in clouds:
        
        #print(np.asarray(cloud.points).shape)
        xyz= np.vstack((xyz, np.asarray(cloud.points)))
        rgb= np.vstack((rgb, np.asarray(cloud.colors)))


    mergedCloud.points = open3d.Vector3dVector(xyz)
    mergedCloud.colors = open3d.Vector3dVector(rgb) #range is 0-1 hence the division

    return mergedCloud

