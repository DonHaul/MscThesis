## rosbag record command

rosbag record --split --size=1024 --duration=1 -b 0 /ervilhamigalhas/depth_registered/points /abretesesamo/depth_registered/points

rosbag record --split --size=1024 --duration=2 -b 0 /ervilhamigalhas/depth_registered/image_raw /abretesesamo/depth_registered/image_raw /ervilhamigalhas/rgb/image_color /abretesesamo/rgb/image_color /abretesesamo/depth/camera_info /ervilhamigalhas/depth/camera_info /ervilhamigalhas/rgb/camera_info /abretesesamo/rgb/camera_info

rosbag record --split --size=1024 --duration=4 -b 0 -a





rosbag record --split --size=1024 --duration=2 -b 0 /camera/depth_registered/image_raw  /camera/rgb/image_color /camera/depth/camera_info /camera/rgb/camera_info


#rgbonly to cameras


rosbag record --split --size=1024 -b 0 /ervilhamigalhas/rgb/image_color /abretesesamo/rgb/image_color /ervilhamigalhas/rgb/camera_info /abretesesamo/rgb/camera_info

