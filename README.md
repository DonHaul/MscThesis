# rosbag record commands

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

### 3 rgb + depth ervilhas abretesesano fernanod
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

