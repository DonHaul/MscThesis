from libs import *
import ObservationsMaker
import numpy as np

class CameraSynthObsMaker2(ObservationsMaker.ObservationsMaker):
    def __init__(self,data):

        self.noiset=data['noiset'] #in meters

        self.Rcangalho=data['synthmodel']['R']
        self.tcangalho=data['synthmodel']['t']


        visu.ViewRefs(data['synthmodel']['R'],data['synthmodel']['t'],refSize=0.1)
        visu.ViewRefs(data['modelscene']['R'],data['modelscene']['t'],refSize=0.1)

        print(len(data['modelscene']['R']))
        self.Rcam=data['modelscene']['R']
        self.tcam=data['modelscene']['t']
        

        self.n_obs = data['samples'] 
        self.noise = 0


        self.n_poses = data['n_poses']
        

        


    def GetObservations(self,streamData):

        

        #similar to output from ROS, gets observations from Marker in the camera coordinate
        camsObs = synth.MultiCamSampleGeneratorFixed(self.Rcam,self.tcam,self.Rcangalho,self.tcangalho,nObs = self.n_obs,noise=self.noise, noiset=self.noiset)

        tmean=np.mean(self.tcam,axis=0)

        print("tmean")
        print(tmean)

        #Rs=[]
        #Ts=[]
        #for i in range(len(self.n_poses)):
        #    Rs.append(mmnip.genRandRotMatrix(360))
        #    Ts.append(tmean+np.random.rand(3,1)*self.noiset)

  

        obsR, obsT = obsgen.GenerateCameraPairObs(camsObs,self.Rcangalho,self.tcangalho)



        return None,None,obsR,obsT
        
