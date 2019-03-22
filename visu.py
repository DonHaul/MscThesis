from matplotlib import pyplot as plt


def plotImg(img):
    fig = plt.figure()
    plt.imshow(img)
    plt.draw()
    plt.waitforbuttonpress()
    plt.close(fig)

def plotImgVid(img):
    plt.imshow(img)
    plt.draw()