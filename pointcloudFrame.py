import open3d
import rosinterface
from sensor_msgs.msg import Image
import rospy
import matmanip as mnip
import pickler as pickle
import pointclouder
import cv2

camsName=["abretesesamo","ervilhamigalhas"]

rospy.init_node('my_name_is_jeff', anonymous=True)

rgbl=[]
depthl=[]

camInfo = pickle.Out("static/CameraInfo 20-04-2019.pickle")

pcl=[]

for i in range(0,len(camsName)):

    
    pc,rgb,depth = rosinterface.GetPointCloudRGBD(camsName[i],camInfo['K'])

    pcl.append(pc)
    rgbl.append(rgb)
    depthl.append(depth)

cv2.imshow("Image window" , rgbl[0])
cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imshow("Image window" , rgbl[1])
cv2.waitKey(0)
cv2.destroyAllWindows()



open3d.draw_geometries([pcl[0]])
open3d.draw_geometries([pcl[1]])
open3d.draw_geometries(pcl)


pcc = pointclouder.MergeClouds(pcl)
print("final PC")
open3d.draw_geometries([pcc])

print("final PC")
    