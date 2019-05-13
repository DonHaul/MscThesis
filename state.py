
class State(object):

    def __init__(self):
        self.__stateDict={}
        self.__SetState({"state":0})

    def __SetState(self,y):
        print("ocurred")
        self.__stateDict.update(y)    # modifies z with y's keys and values & returns None
    

    def PrintState(self):
        print(self.stateDict)


    def __GetState(self):
        return self.__stateDict

    stateDict = property(__GetState, __SetState)

