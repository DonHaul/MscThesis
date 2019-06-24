import PosesCalculator
import numpy as np

class OulierRemovalPoseCalculator(PosesCalculator.PosesCalculator):

    
    def __init__(self,data):

        PosesCalculator.PosesCalculator.__init__(self,data)

        self.n_obs = np.zeros((self.N_objects,),dtype=np.int32)

        self.obsthreshold=data['observations']


        self.Rguess=[]
        self.Tguess=[]

        self.initialguess=True

    def AddObservations(self,obsR,obsT):
        
        for o in obsR:
            self.n_obs[o['to']]=self.n_obs[o['to']]+1
            self.n_obs[o['from']]=self.n_obs[o['from']]+1

        if self.initialguess==True: 


            
            super(OulierRemovalPoseCalculator,self).AddObservations(obsR,obsT)

            if np.count_nonzero(self.n_obs<self.obsthreshold) ==0:

                #reset
                self.n_obs = np.zeros((self.N_objects,),dtype=np.int32)

                if(self.estimating =='R'):
                    self.Rguess = self.CalcRthenStartT()
                elif (self.estimating =='t'):
                    self.Tguess = self.CalcT()
                    
                    self.initialguess=False
                    self.estimating='R'
        else:

            obsRR=[]
            obsTT=[]

            for oR,oT in zip(obsR,obsT):
                    
                print("YAA DATS HOT")
                if self.estimating=='R':

                    RR =  oR['R']-np.dot(self.Rguess[oR['to']].T,self.Rguess[oR['from']])
                    Rnorm = np.linalg.norm(RR)
                    print("RNORM")
                    print(Rnorm)
                elif self.estimating=='t':
                    ttt = np.dot(self.Rguess[oT['from']],(self.Tguess[oT['to']]-self.Tguess[oT['from']]))
                    ttnorm = np.linalg.norm(oT['t']-ttt)
                    print("TNORM")
                    print(ttnorm)
                print("OUTLIER REMOVAL")
            
            
            super(OulierRemovalPoseCalculator,self).AddObservations(obsR,obsT)
            
                


