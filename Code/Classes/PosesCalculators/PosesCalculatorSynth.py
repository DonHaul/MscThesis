import PosesCalculator
import numpy as np

class PosesCalculatorSynth(PosesCalculator.PosesCalculator):
    
    
    def __init__(self,data):

        PosesCalculator.PosesCalculator.__init__(self)


    def AddObservations(self,obsR,obsT):
        
    
        super(PosesCalculatorSynth,self).AddObservations(obsR,obsT)
        super(PosesCalculatorSynth,self).CalcRthenStartT()
        super(PosesCalculatorSynth,self).CalcT()