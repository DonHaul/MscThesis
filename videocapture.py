#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Image
import time

n_capture = 30
count = 0
starttime = time.time()

def callback(data):
	#rospy.loginfo(rospy.get_caller_id() + "I Heard %s", data.data)

	count = count +1

	print("dif",time.time()-starttime)

def listener():
	rospy.init_node('listener', anonymous=True)

	
	print("startstiem",starttime)

	rospy.Subscriber("ervilhamigalhas/depth_registered/image_raw",Image, callback)
	rospy.spin()



if __name__ == '__main__':
	try:
		listener()
	except rospy.ROSInterruptException:
		pass


