import numpy as np
import matmanip
import synth
import probdefs
import algos
import visu


def main():

    np.set_printoptions(threshold=np.inf)
    np.set_printoptions(precision=1)

    R=[]
    t=[]


    R,t = synth.FakeAruco()

    #pprint.pprint(t)

    visu.ViewRefs(R,t)
    
    obsR,obst = synth.SampleGenerator(R,t,noise=0.1,noiset=0,samples=10000)
    #correct

    '''
    for i in obst:
        #print("From: " +str(i['from']//3+1)+" to:"+str(i['to']//3+1))
        print(i)
        #raw_input()
        #ViewRefs([matmanip.genRotMat([0,0,0]),i['trans']])
    '''

    # TRANSLATION STUFF
    A,b = probdefs.translationProbDef(obst,R,len(t))

    #x, res, rank, s = np.linalg.lstsq(A,b,rcond=None) #(A'A)^(-1) * A'b
    x= algos.LeastSquares(A,b)
    #print(x2)

    solsplit2 = np.split(x,len(t))
    visu.ViewRefs(R,solsplit2)


    solt =[]
    #change t referential
    #for i in range(len(solsplit2)):
    #    solt.append(np.dot(-R[i].T,solsplit2[i]))


    #ViewRefs(R,solt)


if __name__ == '__main__':
    main()
