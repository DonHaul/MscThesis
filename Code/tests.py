import libs.FileIO as FileIO


location="./Logs/2019-07-25_16:26:25_pigeon/"

ola = FileIO.getFromPickle(location + "poses.pickle")

print(ola)


FileIO.SaveAsMat(ola,location + "poses.mat")

