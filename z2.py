import json
import numpy as np
import FileIO
import visu
import algos
import matmanip as mmnip
import open3d
mesh_sphere=open3d.create_mesh_sphere(radius = 1.0)
mesh_sphere.paint_uniform_color([1, 0.1, 1])
open3d.draw_geometries([mesh_sphere])