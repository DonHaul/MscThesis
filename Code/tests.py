import libs.FileIO as FileIO


location="./Logs/2019-07-31_19:56:31_weasel/"

ola = FileIO.getFromPickle(location + "poses.pickle")

print(ola)


FileIO.SaveAsMat(ola,location + "poses.mat")

