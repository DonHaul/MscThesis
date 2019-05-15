import algos
import numpy as np
import visu
import matmanip as mmnip

#all variables that can change during the run should be here that are not local
class State(object):

    def __init__(self,N_cams):

        self.N_cams=N_cams
        self.state=0

        self.R=None
        self.t=None


        #A.T A initialized
        self.ATAR = np.zeros((self.N_cams*3,self.N_cams*3))

                #A.T A initialized
        self.ATAt = np.zeros((self.N_cams*3,self.N_cams*3))

        #A.T b initialized
        self.ATb = np.zeros((self.N_cams*3,1))

        self.pc=None

    def CalcRthenStartT(self):
        #if(camposegetter.N_cams==2):
        #    B = camposegetter.lol/g.count
        #    print("2 CAMS")
        #    visu.ViewRefs([np.eye(3),B])
    
        print("global1")
        rotSols = algos.RProbSolv1(self.ATAR,3,self.N_cams)
    
        visu.ViewRefs(rotSols)
        print("global2")
        #rotSols = algos.RProbSolv1(C,3,len(R))    
        #visu.ViewRefs(rotSols)
        
        
        print("local1")    
        rr = mmnip.genRotRelLeft(rotSols)
        visu.ViewRefs(rr)

        self.R=rotSols

        self.state=1

    def CalcT(self):

        x = np.dot(np.linalg.pinv(self.ATAt),self.ATb)
    
        solsplit2 = np.split(x,self.N_cams)
        visu.ViewRefs(self.R,solsplit2,refSize=0.1)

        self.t=solsplit2

