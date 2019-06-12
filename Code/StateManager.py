
import numpy as np

from libs import *


#all variables that can change during the run should be here that are not local
class State(object):

    def __init__(self,N_cams,detectionMode="realtime",camPoses=None,errorCalc=False,PCPath=None,arucoDetection="allforone",recordRT=False):

        self.data={}

        self.N_cams=N_cams
        self.state=0

        self.R=None
        self.t=None

        self.PCPath=PCPath

        self.count=0

        self.R2=np.zeros((3,3))
        self.t2=np.zeros((3,))

        self.showImg=False

        self.detectionMode=detectionMode
        self.readyToCapture=True

        #records R and T between the 2 first cameras
        self.recordedRs=[]
        self.recordedTs=[]

        if self.detectionMode == "snap":
            self.readyToCapture=False

        #it should be either singular, allforone or depthforone
        self.arucoDetection = arucoDetection

        #A.T A initialized
        self.ATAR = np.zeros((self.N_cams*3,self.N_cams*3))

                #A.T A initialized
        self.ATAt = np.zeros((self.N_cams*3,self.N_cams*3))

        #A.T b initialized
        self.ATb = np.zeros((self.N_cams*3,1))

        self.pcs=[]

        self.pc=None

        self.cams={}

        self.snapcount=0

        self.camPoses=camPoses

        #use in one for all mode, one camera from several perspectives
        self.curCam=0



        self.data['errorCalc']=False        

        if errorCalc==True:
            self.data['errorCalc']=True
            self.data['Rs']=[]
            self.data['Ts']=[]

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

        self.state=1

        

    def CalcRT2(self):
        if(self.N_cams==2):
            self.R2 = self.R2/self.count
            print(self.t2.shape)
            self.t2 = self.t2/self.count



            self.R2 = algos.RotCrustes(self.R2,np.eye(3))
        

    def CalcT(self):

        x = np.dot(np.linalg.pinv(self.ATAt),self.ATb)
    
        solsplit2 = np.split(x,self.N_cams)
        
        visu.ViewRefs(self.R,solsplit2,refSize=0.1,showRef=True)

        self.t=solsplit2

