import numpy as np
from libs import *

class GetCangalhoPoses():
    
    def __init__(self,data):

        print("Getting Cangalho")

        self.K=data['K']
        self.D=data['D']
        self.arucoData=data['arucodata']
        

        self.estimating ="R"

        #list of empty lists where observations will be saved (first dim tells camera, second dim is the observations for that cam)
        self.Allobs = []

        #N_objects
        self.N_objects = len(self.arucoData['ids'])

        self.count = 0

        #A.T A initialized
        self.ATAR = np.zeros((self.N_objects*3,self.N_objects*3))

        #A.T A initialized
        self.ATAt = np.zeros((self.N_objects*3,self.N_objects*3))

        #A.T b initialized
        self.ATb = np.zeros((self.N_objects*3,1))


        self.lol=np.zeros((3,3))

        self.arucoData['idmap'] = self.markerIdMapper(self.arucoData['ids'])
        
    def markerIdMapper(self,arr):

        IdMap={}
       
        for i in range(0,len(arr)):
            IdMap[str(arr[i])]=i
       
        return IdMap

    def GetModelPoses(self):

        img,ids,obsR,obsT = aruco.ArucoObservationMaker(img,self.K,self.D,self.Nmarkers,self.arucoData,captureR=True,captureT=True)
        



        #calculates rotations
        if self.estimating == 'R':
            
            #only if there are observations it makes the A matrix
            if  ids is not None and len(ids)>1:
                
                

                A =  probdefs.rotationProbDef(obsR,self.Nmarkers)

                self.ATAR = self.ATAR  + np.dot(A.T,A)

        #calculates translations
        elif self.estimating == 't':
            
            
            if  ids is not None and len(ids)>1:

                A,b =  probdefs.translationProbDef(obsT,self.state.R,self.Nmarkers)

                self.ATAt = self.ATAt + np.dot(A.T,A) #way to save the matrix in a compact manner

                self.ATb = self.ATb + np.dot(A.T,b) #way to save the matrix in a compact manner

        else:
            print("This State does nothing")

        #clear observations
        self.Allobs = []

    def CalcRthenStartT(self):
        #if(camposegetter.N_cams==2):
        #    B = camposegetter.lol/g.count
        #    print("2 CAMS")
        #    visu.ViewRefs([np.eye(3),B])
    
        
        rotSols = algos.RProbSolv1(self.ATAR,3,self.N_cams)
        print("global1")
        #visu.ViewRefs(rotSols)


        

        #converts to world coordinates or into them
        rotSolsNotUsed = mmnip.Transposer(rotSols)

        #converts in first ref coordinates , 
        rr = mmnip.genRotRelLeft(rotSolsNotUsed)

        visu.ViewRefs(rr)

        self.R=rr

        self.estimating='t'

    
    
    def CalcT(self):

        x = np.dot(np.linalg.pinv(self.ATAt),self.ATb)
    
        solsplit2 = np.split(x,self.N_cams)
        
        visu.ViewRefs(self.R,solsplit2,refSize=0.1,showRef=True)

        self.t=solsplit2
