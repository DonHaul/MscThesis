from libs import *

class CamerasObservationMaker:
    def __init__(self,data):

        print("Getting Camera")

        self.intrinsics=data['intrinsics']
        self.arucoData=data['arucodata']
        self.arucoDetection = data['arucodetection']

        self.estimating ="R"

        self.N_objects = len(self.intrinsics['K'])

        self.arucoData['idmap'] = aruco.markerIdMapper(self.arucoData['ids'])


    def GetObservations(self,streamData):

        
        #iterate throguh cameras
        for camId in range(0,self.N_objects):
            
            

            if  self.arucoDetection == "singular":

                img = IRos.rosImg2RGB(args[camId])

                #get observations of this camera, and image with the detected markers and referentials shown
                obs, img = obsgen.Cam2ArucoObsMaker2(img,self.intrinsics['K'][self.camNames[camId]],self.intrinsics['D'][self.camNames[camId]],self.arucoData)

            elif self.arucoDetection == "allforone":
                
                #print("ALL FO ONE")
                img = IRos.rosImg2RGB(args[camId])

                obs, img = obsgen.CamArucoPnPObsMaker(img,self.intrinsics['K'][self.camNames[camId]],self.intrinsics['D'][self.camNames[camId]],self.arucoData,self.arucoModel)
            elif self.arucoDetection == "depthforone":

                
                img = IRos.rosImg2RGB(args[camId*2])
                depth = IRos.rosImg2Depth(args[camId*2+1])
                obs, img = obsgen.CamArucoProcrustesObsMaker(img,self.intrinsics['K'][self.camNames[camId]],self.intrinsics['D'][self.camNames[camId]],self.arucoData,self.arucoModel,depth)
            
            else:
                print("Big Oopsie 5809447652")
                quit()




            #obs = obsGen.FilterGoodObservationMarkerIds(obs,self.R,self.t,len(self.arucoData['idmap']),t_threshold=0.05,R_threshold=0.5)

            #set image
            self.images[0:480,camId*640:camId*640+640,0:3]=img

            #get new observations of that camera
            self.Allobs[camId]=obs  # WRONG SHOULD IT BE concantenate lists OR =?


        #Generate Pairs from all of the camera observations
        obsR , obsT = obsgen.GenerateCameraPairObs(self.Allobs,self.R,self.t)

        return None,None,obsR,obsT
        
