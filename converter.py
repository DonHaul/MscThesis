import open3d
import pypcd
import os


def PC2toOpen3DPC(msg):
    
    pc = pypcd.PointCloud.from_msg(msg)
    pc.save_pcd('aux.pcd',compression='binary_compressed')
    pcdata= open3d.read_point_cloud('aux.pcd')

    os.remove('aux.pcd')

    return pcdata