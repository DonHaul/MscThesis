import rospy



def getAllPluggedCameras():

    cameraNames=[]

    topiclist = rospy.get_published_topics()

    for topic in topiclist:
        
        if "/depth_registered/image_raw" in topic[0] or "/rgb/image_color" in topic[0]:
            name = topic[0].split('/')[1]

            if name not in cameraNames:
                cameraNames.append(name)


    return cameraNames

a = getAllPluggedCameras()


print(a)
