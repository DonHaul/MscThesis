import open3d
from open3d import *
import numpy as np
import copy
import synth

import matmanip as mmnip

import visu 


def main():

    mesh = read_triangle_mesh("models/filmCamera.ply")
    mesh.compute_vertex_normals()
    mesh.paint_uniform_color([1, 0.706, 0])
    #draw_geometries([mesh])
    

    R,t = synth.Scenev1()
    
    t[0] = [0,100,100]


    t[1] = [0,0,-100]

    #visu.ViewRefs(R,t)

    visu.ViewScene(R,t)



    



















if __name__ == '__main__':
    main()