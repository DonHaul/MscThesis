import open3d
import time
import numpy as np

mesh = open3d.read_triangle_mesh("./models/filmCamera.ply")

geos =[]

geos.append(mesh)

open3d.draw_geometries([mesh])

mesh.compute_vertex_normals()
    
open3d.draw_geometries([mesh])

geos[0].paint_uniform_color([1, 0.706, 0])

open3d.draw_geometries(geos)







while True:
    print("gay")

    rand = np.random.rand(3,)
    geos[0].paint_uniform_color(rand)
    open3d.draw_geometries(geos)


    time.sleep(4)


def colorChanger(mesh):
    rand = np.random.rand(3,)
    mesh.paint_uniform_color(rand)

