from libs import *
import ObservationsMaker

class CangalhoSynthObsMaker(ObservationsMaker.ObservationsMaker):
    def __init__(self,arucoData,n_obs,noise):

        self.R=arucoData(0)
        self.t=arucoData(1)
        self.n_obs = n_obs
        self.noise = noise
        pass


    def GetObservations(self,*args):


        obsR,obst = synth.SampleGenerator(R,t,noise=self.noise,samples=self.n_obs)


        return _,_,obsR,obsT
        
