import sys
from libs import *
import numpy as np
import open3d



# This import registers the 3D projection, but is otherwise unused.
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

import matplotlib.pyplot as plt
import numpy as np





def main(argv):

    #Load aruco Model
    transformationz = FileIO.getFromPickle(argv[0])

    #print(transformationz)

    T = np.asarray(transformationz['T'])

    
    print(T.shape)

    
    plt.hist(T[:,0], bins='auto')  # arguments are passed to np.histogram
    plt.title("Histogram with 'auto' bins")
    plt.show()
    
    Tmean = np.mean(T,axis=0)
    Tmedian = np.median(T,axis=0)
    Tstd = np.std(T,axis=0)
    print("Statistics:")
    print("Mean:\t",Tmean)
    print("Median:\t",Tmedian)
    print("Std:\t",Tstd)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(T[:,0],T[:,1],T[:,2], marker='o')

    plt.show()

if __name__ == '__main__':
    main(sys.argv[1:])