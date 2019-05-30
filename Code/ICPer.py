# examples/Python/Bashttp://www.open3d.org/docs/tutorial/reference.html#rusinkiewicz2001ic/icp_registration.py

import open3d as o3d
import numpy as np
import copy

import plyreader

import sys

def draw_registration_result(source, target, transformation):
    source_temp = copy.deepcopy(source)
    target_temp = copy.deepcopy(target)
    #source_temp.paint_uniform_color([1, 0.706, 0])
    #target_temp.paint_uniform_color([0, 0.651, 0.929])
    source_temp.transform(transformation)
    o3d.visualization.draw_geometries([source_temp, target_temp])

def draw_registration_result_original_color(source, target, transformation):
    source_temp = copy.deepcopy(source)
    source_temp.transform(transformation)
    o3d.visualization.draw_geometries([source_temp, target])

if __name__ == "__main__":


    print("Load a ply point cloud, print it, and render it")
    #pcd = read_point_cloud(sys.argv[1])
    #draw_geometries([pcd])

    if ".ply" in sys.argv[1]:
        pcd = read_point_cloud(sys.argv[1])
        o3d.draw_geometries([pcd])
    else:
        pcds = plyreader.load_point_clouds(sys.argv[1])
        o3d.draw_geometries(pcds)
        print("Multi PCs loaded")



    source = pcds[2]
    target = pcds[1]
    
    print("Downsample the point cloud with a voxel of 0.05")
    source = o3d.geometry.voxel_down_sample(source, voxel_size=0.01)
    target = o3d.geometry.voxel_down_sample(target, voxel_size=0.01)

    
    
    o3d.draw_geometries([source])
    o3d.draw_geometries([target])

    

    threshold = 0.02
    trans_init = np.eye(4)
    draw_registration_result(source, target, trans_init)
    print("Initial alignment")
    evaluation = o3d.registration.evaluate_registration(source, target,threshold, trans_init)
    print(evaluation)


    print("Apply point-to-point ICP")
    reg_p2p = o3d.registration.registration_icp(source, target, threshold, trans_init,o3d.registration.TransformationEstimationPointToPoint())
    print(reg_p2p)
    print("Transformation is:")
    print(reg_p2p.transformation)
    print("")
    draw_registration_result(source, target, reg_p2p.transformation)


    print("Recompute the normal of the downsampled point cloud")
    o3d.geometry.estimate_normals(source,search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1,max_nn=30))
    o3d.geometry.estimate_normals(target,search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1,max_nn=30))

    print("Apply point-to-plane ICP")
    reg_p2l = o3d.registration.registration_icp(source, target, threshold, trans_init,o3d.registration.TransformationEstimationPointToPlane())
    print(reg_p2l)
    print("Transformation is:")
    print(reg_p2l.transformation)
    print("")
    
    print(source.normals)
    print(target.normals)

    source.normals=o3d.Vector3dVector([])
    target.normals=o3d.Vector3dVector([])

    draw_registration_result(source, target, reg_p2l.transformation)

    print("ICP COLORED TIME")

    source =pcds[2]
    target = pcds[1]

    voxel_radius = [0.04, 0.02, 0.01]
    max_iter = [50, 30, 14]
    current_transformation = np.identity(4)
    print("3. Colored point cloud registration")
    for scale in range(3):
        iter = max_iter[scale]
        radius = voxel_radius[scale]
        print([iter, radius, scale])

        print("3-1. Downsample with a voxel size %.2f" % radius)
        source_down = o3d.geometry.voxel_down_sample(source, radius)
        target_down = o3d.geometry.voxel_down_sample(target, radius)

        print("3-2. Estimate normal.")
        o3d.geometry.estimate_normals(
            source_down,
            o3d.geometry.KDTreeSearchParamHybrid(radius=radius * 2, max_nn=30))
        o3d.geometry.estimate_normals(
            target_down,
            o3d.geometry.KDTreeSearchParamHybrid(radius=radius * 2, max_nn=30))

        print("3-3. Applying colored point cloud registration")
        result_icp = o3d.registration.registration_colored_icp(
            source_down, target_down, radius, current_transformation,
            o3d.registration.ICPConvergenceCriteria(relative_fitness=1e-6,
                                                    relative_rmse=1e-6,
                                                    max_iteration=iter))
        current_transformation = result_icp.transformation
        print(result_icp)
    
    #source.normals=o3d.Vector3dVector([])
    #target.normals=o3d.Vector3dVector([])
    print(result_icp.transformation)
    draw_registration_result_original_color(source, target,result_icp.transformation)