import numpy as np
import matmanip as mmnip
import synth
import visu

import probdefs
import algos

import scipy.io

import observationgenner as obsgen

def main():


    R,t = synth.FakeArucoReal() #in world coordinates
    
    visu.ViewRefs(R)

    #correct 100%
    obsRR,obstt = synth.SampleGeneratorMultiNoise(R,t,noise=[0.0,0.001,0.01,0.1,1.0],samples=1000)
    #print(len(obsRR[100]))
    print("len pixa")
    print(len(obsRR))


    bigboylist = [[] for i in range(len(obsRR[0]))]

    for obs in obsRR:
        for i in range(0,len(obs)):
            bigboylist[i].append(obs[i])

    print(len(bigboylist[0]))   

    solution=[]
    for obs in bigboylist:
        B = probdefs.rotationProbDef(obs,len(R))
        C=np.dot(B.T,B)
        solution.append( algos.TotalLeastSquares(C,3))
        print("SOLUTION IS")
        #print(solution.shape)
        rotSols = algos.RProbSolv1(C,3,len(R))

        #converts to world coordinates or into them
        rotSolsNotUsed = mmnip.Transposer(rotSols)
        visu.ViewRefs(rotSolsNotUsed)
    

    scipy.io.savemat('output/out.mat', mdict={'leastSignificant_0': solution[0],'leastSignificant_0_001': solution[1],'leastSignificant_0_01': solution[2],'leastSignificant_0_1': solution[3],'leastSignificant_1': solution[4]})



    #rotSols = algos.RProbSolv1(C,3,len(R))
    #visu.ViewRefs(rotSols)

    #converts to world coordinates or into them
    #rotSolsNotUsed = mmnip.Transposer(rotSols)
    #visu.ViewRefs(rotSolsNotUsed)

    #converts in first ref coordinates , 
    #rr = mmnip.genRotRelRight(rotSols)
    #visu.ViewRefs(rr)


    #converts in first ref coordinates , 
    #rr = mmnip.genRotRelLeft(rotSols)
    #visu.ViewRefs(rr)




if __name__ == '__main__':
    main()
