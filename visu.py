from matplotlib import pyplot as plt
import open3d
import numpy as np

def plotImg(img):
    fig = plt.figure()
    plt.imshow(img)
    plt.draw()
    plt.waitforbuttonpress()
    plt.close(fig)


def draw_geometry(pcd):
    # The following code achieves the same effect as:
    # draw_geometries([pcd])
    vis = open3d.Visualizer()

    vis.create_window(width=800 ,height=600)
    opt = vis.get_render_option()
    opt.background_color = np.asarray([0, 0, 0])
    for geo in pcd:
        vis.add_geometry(geo)
    vis.run()
    vis.destroy_window()


def ViewRefs(R=None,t=None,refSize=10, w=None,h=None):

    

    #in case one of them is none, get the one that is not zero
    N = len(R) if R is not None else len(t)

    refs = []

    if t is None:
        t = []
        for i in range(0,N):
            t.append([i*20,0,0]) 



    if R is None:
        R = []
        for i in range(0,N):
            print(R)
            R.append(Rtmat.genRotMat([0,0,0])) 


   

    for i in range(N):

        P=np.eye(4)

        
        P[0:3,0:3]= R[i]
        P[0:3,3]=np.squeeze(t[i])

        refe = open3d.create_mesh_coordinate_frame(refSize, origin = [0, 0, 0])
        refe.transform(P)

        refs.append(refe)

    draw_geometry(refs)

    return refs
