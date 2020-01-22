#!/usr/bin/env python3
from __future__ import print_function

import roslib
import rospy
import rospkg

import std_msgs.msg
from std_msgs.msg import String
from sensor_msgs.msg import Image
from message_filters import TimeSynchronizer, Subscriber
from darknet_ros_msgs.msg import BoundingBoxes
from darknet_ros_msgs.msg import BoundingBox
from kp_detector.msg import Keypoints
from kp_detector.msg import KeypointsList

import sys
from os import listdir
from os.path import isfile, join

import cv2
from cv_bridge import CvBridge, CvBridgeError

import yaml


# def publish_img(pub, img_dir, img_name, bridge, direction,timestamp):
#     img = cv2.imread(img_dir+img_name)
#     if CONFIG["preproc"]:
#         img = cv2.resize(img, (pre_height, pre_width), interpolation=cv2.INTER_CUBIC)
#     ros_img = bridge.cv2_to_imgmsg(img, "bgr8")
#     ros_img.header.stamp=timestamp #rospy.Time.now()
#     rospy.loginfo("print %s '%s' at %d. %d"%(direction,img_name,ros_img.header.stamp.secs,ros_img.header.stamp.nsecs))
#     pub.publish(ros_img)

count = 0

def callback(img0, img1, kps0, kps1):
    global count
    if count >= crop_length:
        print("reached record limit~")
        return
    img_pub_0.publish(img0)
    img_pub_1.publish(img1)
    kps_pub_0.publish(kps0)
    kps_pub_1.publish(kps1)
    count+=1

if __name__ == '__main__':
    
    # load executable path
    # referenced from https://answers.ros.org/question/236116/how-do-i-access-files-in-same-directory-as-executable-python-catkin/
    pwd = rospkg.RosPack().get_path("img_publisher")+"/"

    # load config yaml file 
    with open(pwd+"config.yaml","r") as f:
        CONFIG=yaml.load(f)

    # work in stereo mode
    img_pub_0 = rospy.Publisher(CONFIG["img_topic_0"], Image, queue_size=100)
    img_pub_1 = rospy.Publisher(CONFIG["img_topic_1"], Image, queue_size=100)
    kps_pub_0 = rospy.Publisher(CONFIG["kps_data_0"], KeypointsList, queue_size=100)
    kps_pub_1 = rospy.Publisher(CONFIG["kps_data_1"], KeypointsList, queue_size=100)
    
    rospy.init_node('cropper',anonymous=True)
    crop_length=CONFIG["crop_length"]

    tss_0 = TimeSynchronizer([Subscriber(CONFIG["img_topic_0_remap"], Image),
                            Subscriber(CONFIG["img_topic_1_remap"], Image),
                            Subscriber(CONFIG["kps_data_0_remap"], KeypointsList),
                            Subscriber(CONFIG["kps_data_1_remap"], KeypointsList)],200)
    tss_0.registerCallback(callback)
    rospy.spin()

    # rate = rospy.Rate(CONFIG["hz"])

    # # I don't know why we have to set image scale fixed
    # # Or else it seems like the yolo will fail at recognize varied scales imgs(you can try comment cv2.resize(..))
    # pre_width=CONFIG["pre_width"]
    # pre_height=CONFIG["pre_height"]
    
    # # fetch the image name lists
    # name_list_0=[]
    # name_list_1=[]
    # if CONFIG["list_path_0"]!="":
    #     with open(CONFIG["list_path_0"],"r") as f_0:
    #         name_list_0 = f_0.readlines()
    #     with open(CONFIG["list_path_1"],"r") as f_1:
    #         name_list_1 = f_1.readlines()
    #     if CONFIG["parser_mode"]=="tum":
    #         name_list_0 = [x.strip().split(" ")[1] for x in name_list_0 if x.strip().startswith("#")==False]
    #         name_list_1 = [x.strip().split(" ")[1] for x in name_list_1 if x.strip().startswith("#")==False]
    #     else:
    #         name_list_0 = [x.strip() for x in name_list_0 if x.strip().startswith("#")==False]
    #         name_list_1 = [x.strip() for x in name_list_1 if x.strip().startswith("#")==False]
    # else:
    #     name_list_0 = [fi_0 for fi_0 in listdir(CONFIG["dir_path_0"]) if isfile(join(CONFIG["dir_path_0"],fi_0))]
    #     name_list_0.sort()
    #     name_list_1 = [fi_1 for fi_1 in listdir(CONFIG["dir_path_1"]) if isfile(join(CONFIG["dir_path_1"],fi_1))]
    #     name_list_1.sort()

    # # check if two list don't have same amount of images
    # if len(name_list_0)!=len(name_list_1):
    #     print("left and right camera don't have same number of images, exit!")
    #     exit()
    
    # # start publishing loop
    # bridge=CvBridge()
    # idx = 0
    # while not rospy.is_shutdown():
    #     if idx == len(name_list_0) or idx == CONFIG["pub_img_max"]:
    #         input("the file has touched the end, press any key to reset!")
    #         idx = 0

    #     timestamp=rospy.Time.now() # for convenience of synchronize
    #     publish_img(pub_0, CONFIG["dir_path_0"], name_list_0[idx], bridge, "left ",timestamp)
    #     publish_img(pub_1, CONFIG["dir_path_1"], name_list_1[idx], bridge, "right",timestamp)
        
    #     idx+=1
    #     rate.sleep()
