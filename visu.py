"""
visu.py

This module contains functions to visualize plots, Referentials and pointclouds
"""

from matplotlib import pyplot as plt
import open3d
import numpy as np
import matmanip as mmnip


def plotImg(img):
    '''
    receives an image and plots it.

    Upon pressing key plot closes
    '''
    fig = plt.figure()
    plt.imshow(img)
    plt.draw()
    plt.waitforbuttonpress()
    plt.close(fig)

def draw_non_blocking():
    pass


def draw_geometry(pcd):
    '''
    Draws an open3d geometry with a black bacground so that my eyes dont bleed out.
    Upon pressing Escape, the plot closes.

    Args:
        pcd [open3d.Geometry]: Array of geometries to display

    Returns:
        Visualizer: the generates Visualizer window
    '''
    # The following code achieves the same effect as:
    # draw_geometries([pcd])
    vis = open3d.Visualizer()

    #creates the window
    vis.create_window(width=800 ,height=600)

    #fetches its options
    opt = vis.get_render_option()

    #makes it black
    opt.background_color = np.asarray([0, 0, 0])
    for geo in pcd:
        vis.add_geometry(geo)

    #applies all geometries
    vis.run()
    vis.destroy_window()

    return vis

def ViewRefs(R=None,t=None,refSize=10,showRef=False,view=True,zaWordu=False):
    '''ViewRefs - Displays a bunch of referentials on the screen

    Args:
        R: Rotations Array from the world to it
        t: Translations Array from the each referential in world coordinated
        refSize: Size of the referentials
    '''
    

    #in case one of them is none, get the one that is not zero
    N = len(R) if R is not None else len(t)

    refs = []

    #When no t is given, generate translations in a line
    if t is None:
        t = []
        for i in range(0,N):
            t.append([i*20,0,0]) 


    #When no R is given, generate Rotations with no rotation (Identity)
    if R is None:
        R = []
        for i in range(0,N):
            print(R)
            R.append(mmnip.genRotMat([0,0,0])) 


   
    #display each referential (R,t)
    for i in range(N):
        
        P=np.eye(4)                 #Initialize P matrix - homographic transformation

        #print(P.shape)
        #print("thing shape")
        #print(P[0:3,0:3].shape)
        #print(R[i])
        P[0:3,0:3]= R[i]            #Set R
        P[0:3,3]=np.squeeze(t[i])   #Set t

        #Create referential mesh
        refe = open3d.create_mesh_coordinate_frame(refSize, origin = [0, 0, 0])
        
        
        refe.transform(P)   #Transform it according tom p

        refs.append(refe)   #Add it to the Referentials array

    if(showRef==True):
        mesh_sphere=open3d.create_mesh_sphere(radius = refSize*0.3)

        P=np.eye(4)                 #Initialize P matrix - homographic transformation
        P[0:3,0:3]= R[0]            #Set R
        P[0:3,3]=np.squeeze(t[0])   #Set t

        mesh_sphere.transform(P)
        mesh_sphere.paint_uniform_color([1, 0.1, 1])
        refs.append(mesh_sphere)

    if(zaWordu==True):
        refe = open3d.create_mesh_coordinate_frame(refSize*0.2, origin = [0, 0, 0])
        refs.append(refe)

    if view==True:
        draw_geometry(refs) #Draw them all

    return refs
