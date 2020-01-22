#!/usr/bin/env python3
from __future__ import print_function

import roslib
import rospy
import rospkg

import std_msgs.msg
from std_msgs.msg import String
from sensor_msgs.msg import Image
from sensor_msgs.msg import Imu
from geometry_msgs.msg import Vector3

import sys
from os import listdir
from os.path import isfile, join

import cv2
from cv_bridge import CvBridge, CvBridgeError

import yaml
import time
import datetime

def publish_img(pub, img_dir, img_name, bridge, direction,timestamp):
    img = cv2.imread(img_dir+img_name)
    if CONFIG["preproc"]:
        img = cv2.resize(img, (pre_height, pre_width), interpolation=cv2.INTER_CUBIC)
    ros_img = bridge.cv2_to_imgmsg(img, "bgr8")
    ros_img.header.stamp=timestamp #rospy.Time.now()
    rospy.loginfo("print %s '%s' at %d. %d"%(direction,img_name,ros_img.header.stamp.secs,ros_img.header.stamp.nsecs))
    pub.publish(ros_img)

def publish_imu(pub, imu_dir, imu_name, timestamp):
    ros_imu = Imu()
    ros_imu.header.stamp=timestamp
    reader= open(imu_dir+imu_name,"r")
    lines = reader.readlines()
    datalist=list(map(float, lines[0].strip().split(" ")))
    ros_imu.orientation_covariance = [-1,0,0, 0,0,0, 0,0,0]
    angular_velocity=Vector3()
    angular_velocity.x=datalist[17]
    angular_velocity.y=datalist[18]
    angular_velocity.z=datalist[19]
    linear_acceleration=Vector3()
    linear_acceleration.x=datalist[11]
    linear_acceleration.y=datalist[12]
    linear_acceleration.z=datalist[13]
    ros_imu.angular_velocity = angular_velocity
    ros_imu.linear_acceleration = linear_acceleration
    rospy.loginfo("print IMU '%s' at %d. %d"%(imu_name,ros_imu.header.stamp.secs,ros_imu.header.stamp.nsecs))
    pub.publish(ros_imu)
    reader.close()

if __name__ == '__main__':
    
    # load executable path
    # referenced from https://answers.ros.org/question/236116/how-do-i-access-files-in-same-directory-as-executable-python-catkin/
    pwd = rospkg.RosPack().get_path("img_publisher")+"/"

    # load config yaml file 
    with open(pwd+"config.yaml","r") as f:
        CONFIG=yaml.load(f)


    # work in stereo mode
    pub_0 = rospy.Publisher(CONFIG["img_topic_0"], Image, queue_size=100)
    pub_1 = rospy.Publisher(CONFIG["img_topic_1"], Image, queue_size=100)
    pub_imu = rospy.Publisher(CONFIG["imu_topic"], Imu, queue_size=100)
    rospy.init_node('img_publisher')
    rate = rospy.Rate(CONFIG["hz"])

    # I don't know why we have to set image scale fixed
    # Or else it seems like the yolo will fail at recognize varied scales imgs(you can try comment cv2.resize(..))
    pre_width=CONFIG["pre_width"]
    pre_height=CONFIG["pre_height"]
    
    # fetch the image name lists
    name_list_0=[]
    name_list_1=[]
    if CONFIG["list_path_0"]!="":
        with open(CONFIG["list_path_0"],"r") as f_0:
            name_list_0 = f_0.readlines()
        with open(CONFIG["list_path_1"],"r") as f_1:
            name_list_1 = f_1.readlines()
        if CONFIG["parser_mode"]=="tum":
            name_list_0 = [x.strip().split(" ")[1] for x in name_list_0 if x.strip().startswith("#")==False]
            name_list_1 = [x.strip().split(" ")[1] for x in name_list_1 if x.strip().startswith("#")==False]
        else:
            name_list_0 = [x.strip() for x in name_list_0 if x.strip().startswith("#")==False]
            name_list_1 = [x.strip() for x in name_list_1 if x.strip().startswith("#")==False]
    else:
        name_list_0 = [fi_0 for fi_0 in listdir(CONFIG["dir_path_0"]) if isfile(join(CONFIG["dir_path_0"],fi_0))]
        name_list_0.sort()
        name_list_1 = [fi_1 for fi_1 in listdir(CONFIG["dir_path_1"]) if isfile(join(CONFIG["dir_path_1"],fi_1))]
        name_list_1.sort()
        if CONFIG["enable_imu"]:
            name_list_imu = [fi_imu for fi_imu in listdir(CONFIG["dir_path_imu"]) if isfile(join(CONFIG["dir_path_imu"],fi_imu))]
            name_list_imu.sort()

    # check if two list don't have same amount of images
    if len(name_list_0)!=len(name_list_1):
        print("left and right camera don't have same number of images, exit!")
        exit()
    
    if CONFIG["enable_imu"]:
        with open(CONFIG["imu_stamp_file"],"r") as reader:
            imu_lines = reader.readlines()

    # start publishing loop
    bridge=CvBridge()
    idx = 0
    zero_repe=5 # publish several first frames, as yolo3ros is stupid...
    while not rospy.is_shutdown():
        if zero_repe>0:
            zero_repe-=1
        if idx == len(name_list_0) or idx == CONFIG["pub_img_max"]:
            input("the file has touched the end, press any key to reset!")
            idx = 0
            zero_repe=5
        if CONFIG["enable_imu"]:
            # then we need to read in from timestamp list file
            raw_date_str = imu_lines[idx].strip().split(".")
            if zero_repe<=1:
                sec = time.mktime(datetime.datetime.strptime(raw_date_str[0],"%Y-%m-%d %H:%M:%S").timetuple())
                nsec = int(raw_date_str[1])
            else:
                # for first several frames, avoid to let them overwrite the real sem outputs
                sec=0
                nsec=0
            timestamp = rospy.Time.now()
            timestamp.secs = int(sec)
            timestamp.nsecs = nsec
        else:
            timestamp = rospy.Time.now() # for convenience of synchronize
        publish_img(pub_0, CONFIG["dir_path_0"], name_list_0[idx], bridge, "left ",timestamp)
        publish_img(pub_1, CONFIG["dir_path_1"], name_list_1[idx], bridge, "right",timestamp)
        if CONFIG["enable_imu"]:
            publish_imu(pub_imu, CONFIG["dir_path_imu"],name_list_imu[idx], timestamp)
        if zero_repe<=0:
            idx+=1
        rate.sleep()
