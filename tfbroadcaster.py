import roslib
import rospy
import FileIO

import tf
import cv2
from geometry_msgs.msg import Pose

import matmanip as mmnip
import numpy as np

#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String

def main():

    scene = FileIO.LoadScene("./scenes/eland 15-05-2019 02:14:29.json")
    #print(scene)
    #quit()

    H = mmnip.Rt2Homo(scene[0][0])
    print(H)
    print(tf.transformations.quaternion_from_matrix(H))
    print(tf.transformations.translation_from_matrix(H))


    #pub = rospy.Publisher('chatter', Pose, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        
        for i in range(0,len(scene[2])):

            H = mmnip.Rt2Homo(scene[0][i],np.squeeze(scene[1][i]))

            br = tf.TransformBroadcaster()
            br.sendTransform(tf.transformations.translation_from_matrix(H),
                            tf.transformations.quaternion_from_matrix(H),
                            rospy.Time.now(),
                            scene[2][i],
                            "world")
            hello_str = "hello world %s" % rospy.get_time()
            #rospy.loginfo(hello_str)
            #pub.publish(hello_str)
            rate.sleep()
            print("sending tf")

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass