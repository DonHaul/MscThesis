from libs import *

class CamerasObservationMaker:
    def __init__(self,data):

        print("Getting Camera")

        self.intrinsics=data['intrinsics']
        self.arucoData=data['arucodata']

        self.camNames = data['camnames']
        self.arucoModel = data['arucomodel']

        self.estimating ="R"

        self.N_objects = len(self.intrinsics['K'])

        self.arucoData['idmap'] = aruco.markerIdMapper(self.arucoData['ids'])

        self.Allobs = [ [] for i in range(self.N_objects) ]


        self.arucoDetector =  data["innerpipeline"]['arucodetector']




    def GetObservations(self,streamData):
        
        #iterate throguh cameras
        for camId in range(0,self.N_objects):
            
            streamsingle = {
                'rgb':streamData['rgb'][camId],
                'depth':streamData['depth'][camId]
            }
            

            obs,img = self.arucoDetector.ArucoDetector(streamsingle,self.intrinsics['K'][self.camNames[camId]],self.intrinsics['D'][self.camNames[camId]])




            #get new observations of that camera
            self.Allobs[camId]=obs  # WRONG SHOULD IT BE concantenate lists OR =?


        #Generate Pairs from all of the camera observations
        obsR , obsT = obsgen.GenerateCameraPairObs(self.Allobs,self.arucoModel['R'],self.arucoModel['T'])


        #clear observations
        self.Allobs = [ [] for i in range(self.N_objects) ]

        return None,None,obsR,obsT
        
