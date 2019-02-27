class CamData:
    rgb = None
    dept = None
    kp =None
    des=None

    def __init__(self, rgbImg, depthImg):
        self.rgb = rgbImg
        self.depth = depthImg