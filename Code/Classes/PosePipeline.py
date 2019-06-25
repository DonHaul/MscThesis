class PosePipeline():

    def __init__(self):
        self.imgStream={}
        self.ObservationMaker={}
        self.posescalculator={}
        
        self.stop_threads = False

        self.GetStop = lambda : self.stop_threads
        self.folder =""

    def Stop(self):
        self.stop_threads=True
        
    
    def imgShower(self,data):

        rows=1
        colunms=len(data['rgb'])
        
        if len(data['depth'])>0:
            rows=rows+1
        
        shape = data['rgb'][0].shape
        imgs =  np.zeros((shape[0]*rows,shape[1]*colunms,3),dtype=np.uint8)



        for i in range(colunms):
            imgs[0:shape[0],shape[1]*i:shape[1]*(i+1),0:3]=data['rgb'][i]
            #imgs[shape[0]*1:shape[0]*(1+1),shape[1]*i:shape[1]*(i+1),0]=data['depth'][i]



        cv2.imshow('image',imgs)
        cv2.waitKey(10)
        
