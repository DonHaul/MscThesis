import rospy
import numpy as np
from sensor_msgs.msg import PointCloud2
from ast import literal_eval
import struct
from matplotlib import pyplot as plt

rospy.init_node('my_name_is_jeff', anonymous=True)


topicDepth ="ervilhamigalhas/depth_registered/points"


msg = rospy.wait_for_message(topicDepth, PointCloud2)

print("header",msg.header)

print("fields",msg.fields)

print("height",msg.height)
print("width",msg.width)
print("pointstep",msg.point_step)
print("rowstep",msg.row_step)
print("dense",msg.is_dense)
print("length",len(msg.data))

#9830400/32/640 = 480
#rowstep = 32*640

r=[]
g=[]
b=[]
alpha=[]

count = 0

#point step example (32 bytes)
#\x00\x00\xc0\x7f - x
#\x00\x00\xc0\x7f - y
#\x00\x00\xc0\x7f - z
#\x00\x00\x00\x00 - nothing
#Zjt\xff          - rgba
#\x00\x00\x00\x00 - nothing
#\x00\x00\x00\x00 - nothing
#\x00\x00\x00\x00 - nothing

# 2457600 e 480 x 640
print("============================")
inioff=4
for i in range(0, msg.height*msg.width):

    x = msg.data[i*msg.point_step:i*msg.point_step+4]
    y = msg.data[i*msg.point_step+4:i*msg.point_step+4+4]
    z = msg.data[i*msg.point_step+4+4:i*msg.point_step+4+4+4]
    rgb = msg.data[i*msg.point_step+4+4+4+4:i*msg.point_step+4+4+4+4+4]

    #print("x",x)
    #print("y",y)
    #print("z",z)
    #print("c",rgb)

    #boi = struct.unpack('!f', mss)
    #print("fetched",boi)

       
    r.append(ord(rgb[0])) #com ou sem 255-
    g.append(ord(rgb[1]))
    b.append(ord(rgb[2]))
    alpha.append(ord(rgb[3   ]))

    #count=count+1
    #print(count)


print(len(r))


r = np.asarray(r)
g = np.asarray(g)
b = np.asarray(b)
alpha = np.asarray(alpha)

print("heya",alpha[1:])

r=r.reshape(480,-1)
g=g.reshape(480,-1)
b=b.reshape(480,-1)
alpha=alpha.reshape(480,-1)


image = np.array([r,g,b])#alpha must be added

image = np.transpose(image, (1, 2, 0))
print(image.shape)
print(image[:,:,0])



plt.imshow(image,alpha=1)
plt.show()