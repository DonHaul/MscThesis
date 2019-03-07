import rospy
import numpy as np
from sensor_msgs.msg import PointCloud2


rospy.init_node('my_name_is_jeff', anonymous=True)


topicDepth ="ervilhamigalhas/depth_registered/points"


msg = rospy.wait_for_message(topicDepth, PointCloud2)

    
    