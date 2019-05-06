# examples/Python/Advanced/non_blocking_visualization.py

from open3d import *
import numpy as np
import copy

def colorChanger(mesh):
    rand = np.random.rand(3,)
    mesh.paint_uniform_color(rand)

if __name__ == "__main__":

    set_verbosity_level(VerbosityLevel.Debug)
    source = read_triangle_mesh("./models/filmCamera.ply")
    

    draw_geometries([source])

    vis = Visualizer()
    vis.create_window()
    
    vis.add_geometry(source)
    while True:
        
        colorChanger(source)

        vis.update_geometry()
        vis.poll_events()
        vis.update_renderer()
    vis.destroy_window()

vis.add_geometry(source)


