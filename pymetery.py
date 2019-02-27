    
    fig = plt.figure()
    plt.imshow(cv_rgb1)
    plt.show()
    plt.draw()



    # used to  compare obtained pc from depth and rgb img with the ros one


    topicPC ="/depth_registered/points"   
    pcmsg = rospy.wait_for_message(cameraNames[0] + topicPC, PointCloud2)

    truecloud = converter.PC2toOpen3DPC(pcmsg)

    open3d.draw_geometries([truecloud,pcd])
    