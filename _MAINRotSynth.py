import numpy as np
import matmanip as mmnip
import synth
import visu

import probdefs
import algos

def main():

    np.set_printoptions(threshold=np.inf)
    np.set_printoptions(precision=1)

    R,t = synth.FakeAruco()

    visu.ViewRefs(R,t)


    #correct 100%
    obsR,obst = synth.SampleGenerator(R,t,noise=0.1)

    '''
    for i in obsR:
        print("From: " +str(i['from']//3+1)+" to:"+str(i['to']//3+1))
        print(i)
        ViewRefs([Rtmat.genRotMat([0,0,0]),i['rot']])
    '''

    B = probdefs.rotationProbDef(obsR,len(R))  #95% confidence that it is correct

    C = np.dot(B.T,B) #C = B'B


    rotSols = algos.TotalLeastSquares(C,3,len(R)) 

    print("global")

    visu.ViewRefs(rotSols)

    print("local")
    
    rotSoles = mmnip.genRotRel(rotSols)
    
  
    #see R between each things
    for j in range(0,len(rotSoles)):
        r = rotSoles
        print(str(j)+":")
        print(r)





    #print("local")
    visu.ViewRefs(rotSoles)

    #comparing with ground truth
    

if __name__ == '__main__':
    main()
