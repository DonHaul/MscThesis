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

    visu.ViewRefs(R)

    groundTruths = mmnip.genRotRel(R) #95% confidence that it is correct
    
    visu.ViewRefs(groundTruths)


    #correct
    obsR,obst = synth.SampleGenerator(R,t,noise=0.1)

    '''
    for i in obsR:
        print("From: " +str(i['from']//3+1)+" to:"+str(i['to']//3+1))
        print(i)
        ViewRefs([Rtmat.genRotMat([0,0,0]),i['rot']])
    '''

    B = probdefs.rotationProbDef(obsR,len(R))  #95% confidence that it is correct

    C = np.dot(B.T,B) #C = B'B


    rotSols = algos.TotalLeastSquares(C,3,len(R)) #<- HAS TO BE WRONG
    
    print("global")

    visu.ViewRefs(rotSols)

    print("local")


    
    rotSoles = [] #correct way to make 2d list

    #generate R between each things
    for j in range(0,len(rotSols)):
        rotSoles.append(np.dot(rotSols[j].T,rotSols[0])) #Rw2*R1w' = R12  


    #print("local")
    visu.ViewRefs(rotSoles)

    #comparing with ground truth
    

if __name__ == '__main__':
    main()
