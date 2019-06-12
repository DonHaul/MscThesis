import sys
from libs import *
import numpy as np
import open3d

from shutil import copyfile

import csv

# This import registers the 3D projection, but is otherwise unused.
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

import matplotlib.pyplot as plt
import numpy as np





def main(argv):

    #Load aruco Model
    transformationz = FileIO.getFromPickle(argv[1])

    filename=FileIO.GetFileName(argv[1])

    

    folderpath = FileIO.CreateFolder("errors/"+filename) +"/"

    copyfile(argv[1],folderpath+"data.pickle")

    print(folderpath)
    T = np.asarray(transformationz['T'])

    R = np.asarray(transformationz['R'])
    R = R.reshape((R.shape[0],9))


    features = np.concatenate((T,R),axis=1)

    names = ["X","Y","Z","R00","R01","R02","R10","R11","R12","R20","R21","R22"]


    #1 id per sample
    print(R.shape)
    x= range(len(T[:,1]))
    
    featuresMean = np.mean(features,axis=0)
    featuresMedian = np.median(features,axis=0)
    featuresStd = np.std(features,axis=0)

    with open(folderpath+'statistics.csv', 'w') as csvfile:
        stats = csv.writer(csvfile, delimiter=';')
        stats.writerow(['Values','Mean','Std','Median'])

        for i in range(len(names)): 
            stats.writerow([names[i],featuresMean[i],featuresStd[i],featuresMedian[i]])
            
    
    
    #Saves Translations
    for i in range(len(names)):    


        color = (0.2, 0.4, 0.6, 1)

        #Draws BarPlot
        fig_object = plt.figure(figsize=(1920/80.0, 1080/80.0), dpi=80)
        plt.bar(x,features[:,i],width=1.0,edgecolor=color, color=color)
        plt.title(names[i]+" over Time")

        FileIO.SaveImageAllFormats(fig_object,names[i]+"_in_time",folderpath)

        plt.show(block=False)
        plt.pause(1)
        plt.close()
        
        #Draws Histogram
        fig_object = plt.figure(figsize=(1920/80.0, 1080/80.0), dpi=80)
        plt.hist(features[:,i], bins=100,color=color)  # arguments are passed to np.histogram
        plt.title("Histogram of "+names[i])
        FileIO.SaveImageAllFormats(fig_object,names[i]+"_hist",folderpath)

        plt.show(block=False)
        plt.pause(1)
        plt.close()
    



    #fig = plt.figure()
    #ax = fig.add_subplot(111, projection='3d')
    #ax.scatter(T[:,0],T[:,1],T[:,2], marker='o')
    #plt.show()

if __name__ == '__main__':
    main(sys.argv)