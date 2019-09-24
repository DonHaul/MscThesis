# rosbag record commands
rostopic echo /speedwagon/rgb/image_rect_color/header/stamp

Reference this pacckages somewhere:
https://pypi.org/project/MultiCamCalAruco/ this link has python project, update prepared package later
https://github.com/DonHaul/MultiCamCalAruco


### eveything
rosbag record --split --size=1024 --duration=4 -b 0 -a

### 2 camerainfoRGB + camerainfoDepth
rosbag record --split --size=1024 -b 0 /abretesesamo/rgb/camera_info /ervilhamigalhas/rgb/camera_info /ervilhamigalhas/depth/camera_info /abretesesamo/depth/camera_info

### 1 rgb + camera_params
rosbag record --split --size=1024 -b 0 /abretesesamo/rgb/image_color /abretesesamo/rgb/camera_info

### 2 rgb 
rosbag record --split --size=1024 -b 0 /abretesesamo/rgb/image_color /ervilhamigalhas/rgb/image_color

### 1 rgb + depth
rosbag record --split --size=1024 -b 0 /camera/depth_registered/image_raw  /camera/rgb/image_color 

### 2 pc2
rosbag record --split --size=1024 -b 0 /ervilhamigalhas/depth_registered/points /abretesesamo/depth_registered/points

### 2 rgb + depth
rosbag record --split --size=1024 -b 0 /ervilhamigalhas/depth_registered/image_raw /abretesesamo/depth_registered/image_raw /ervilhamigalhas/rgb/image_color /abretesesamo/rgb/image_color

### 3 rgb + depth ervilhas abretesesano fernanod
rosbag record --split --size=2048 -b 0 /ervilhamigalhas/depth_registered/image_raw /abretesesamo/depth_registered/image_raw /fernando/depth_registered/image_raw /ervilhamigalhas/rgb/image_color /abretesesamo/rgb/image_color /fernando/rgb/image_color

### 3 rgb + depth ervilhas abretesesamo fernanod
rosbag record --split --size=2048 -b 0 /ervilhamigalhas/depth_registered/image_raw /ervilhamigalhas/rgb/image_color /abretesesamo/depth_registered/image_raw abretesesamo/rgb/image_color /fernando/rgb/image_color /fernando/depth_registered/image_raw/

### 3 rgb + depth ervilhas abretesesano quim
rosbag record --split --size=2048 -b 0 /ervilhamigalhas/depth_registered/image_raw /ervilhamigalhas/rgb/image_color /abretesesamo/depth_registered/image_raw abretesesamo/rgb/image_color /quim/rgb/image_color /quim/depth_registered/image_raw/

### 3 rgb + depth ervilhas quim fernanod
rosbag record --split --size=2048 -b 0 /ervilhamigalhas/depth_registered/image_raw /ervilhamigalhas/rgb/image_color /quim/depth_registered/image_raw quim/rgb/image_color /fernando/rgb/image_color /fernando/depth_registered/image_raw/


### 3 rgb + depth abrete quim fernanod
rosbag record --split --size=2048 -b 0 /abretesesamo/depth_registered/image_raw /abretesesamo/rgb/image_color /quim/depth_registered/image_raw quim/rgb/image_color /fernando/rgb/image_color /fernando/depth_registered/image_raw/


### 2 rgb + depth + pc2
rosbag record --split --size=2048 -b 0 /ervilhamigalhas/depth_registered/image_raw /abretesesamo/depth_registered/image_raw /ervilhamigalhas/rgb/image_color /abretesesamo/rgb/image_color /ervilhamigalhas/depth_registered/points /abretesesamo/depth_registered/points


### camera calibration  script

rosrun camera_calibration cameracalibrator.py --size 8x6 --square 0.042 image:=/ervilhamigalhas/rgb/image_color camera:=ervilhamigalhas --no-service-check
rosrun camera_calibration cameracalibrator.py --size 8x6 --square 0.042 image:=/quim/rgb/image_color camera:=quim --no-service-check

### quim rgb + depth
rosbag record --split --size=1024 -b 0 /quim/depth_registered/image_raw  /quim/rgb/image_color 

##
rosrun rqt_tf_tree rqt_tf_tree 

aruco normals diagonal:(real)
first face (2,3,4) : 0.300 m
second face (5,6,7) : 0.296 m
second face (8,9,10) : 0.29 m
second face (11,12,13) : 0.294 m

do modelo captado
0.30318389030032905
0.2979090065279915
0.2921658037606405
0.2959685667815067

## kinect mode
rosbag record --split --size=2048 -b 0 /camera/depth/points /camera/depth_registered/points /camera/rgb/raw /camera/depth/image_raw /camera/rgb/image_raw /tf_static


## 2 realsenseki2nect mode
rosbag record --split --size=2048 -b 0 /speedwagon/rgb/image_rect_color /speedwagon/depth_registered/sw_registered/image_rect_raw /emperorcrimson/rgb/image_rect_color /emperorcrimson/depth_registered/sw_registered/image_rect_raw

## 5 realsenseki2nect mode 5cams rgb+depth
rosbag record --split --size=4096 -b 0 /speedwagon/rgb/image_rect_color /speedwagon/depth_registered/sw_registered/image_rect_raw /emperorcrimson/rgb/image_rect_color /emperorcrimson/depth_registered/sw_registered/image_rect_raw /mista/rgb/image_rect_color /mista/depth_registered/sw_registered/image_rect_raw /killerqueen/rgb/image_rect_color /killerqueen/depth_registered/sw_registered/image_rect_raw /diavolo/rgb/image_rect_color /diavolo/depth_registered/sw_registered/image_rect_raw

## 4 realsenseki2nect mode 5cams rgb+depth
rosbag record --split --size=4096 -b 0 /speedwagon/rgb/image_rect_color /speedwagon/depth_registered/sw_registered/image_rect_raw /emperorcrimson/rgb/image_rect_color /emperorcrimson/depth_registered/sw_registered/image_rect_raw /mista/rgb/image_rect_color /mista/depth_registered/sw_registered/image_rect_raw image_rect_raw /diavolo/rgb/image_rect_color /diavolo/depth_registered/sw_registered/image_rect_raw


## 5 realsenseki2nect mode 5cams rgb+depth+pc
rosbag record --split --size=4096 -b 0 /speedwagon/rgb/image_rect_color /speedwagon/depth_registered/sw_registered/image_rect_raw /emperorcrimson/rgb/image_rect_color /emperorcrimson/depth_registered/sw_registered/image_rect_raw /mista/rgb/image_rect_color /mista/depth_registered/sw_registered/image_rect_raw /killerqueen/rgb/image_rect_color /killerqueen/depth_registered/sw_registered/image_rect_raw /diavolo/rgb/image_rect_color /diavolo/depth_registered/sw_registered/image_rect_raw /speedwagon/depth/points /speedwagon/depth_registered/points /emperorcrimson/depth/points /emperorcrimson/depth_registered/points /mista/depth/points /mista/depth_registered/points  /killerqueen/depth/points /killerqueen/depth_registered/points  /diavolo/depth/points /diavolo/depth_registered/points 


