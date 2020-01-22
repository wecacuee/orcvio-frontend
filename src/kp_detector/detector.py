#!/usr/bin/env python3

from __future__ import print_function
from functools import reduce

import roslib
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from message_filters import TimeSynchronizer, Subscriber
from darknet_ros_msgs.msg import BoundingBoxes
from darknet_ros_msgs.msg import BoundingBox
from kp_detector.msg import Keypoints
from kp_detector.msg import KeypointsList

import tensorflow as tf
import numpy as np
from tensorflow.python.tools import inspect_checkpoint as chkp

import yaml
import time
import sys
import os

# Find exec path
import os, rospkg
rp = rospkg.RosPack()
pwd = rp.get_path("kp_detector")+"/"

# Load semantic classes
index_list=[[0,1,2,3,4,5,6,7],
            [8,9,10,11,12,13,14,15,16,17],
            [18,19,20,21,22,23,24,25],
            [26,27,28,29,30,31,32],
            [33,34,35,36,37,38,39,40,41,42,43,44],
            [45,46,47,48,49,50,51,52,53,54,55,56],
            [57,58,59,60,61,62,63,64,65,66],
            [67,68,69,70,71,72,73,74,75,76],
            [77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93],
            [94,95,96,97,98,99,100,101]]

class_list=["aeroplane", "bicycle", "boat", "bottle", "bus",
            "car", "chair", "sofa", "train", "tvmonitor"]
semantic_d={key:value for (key,value) in zip(class_list,index_list)}


def get_publish_data(image, boundingboxes):
  vis_image=None
  out_img_tmp_list=[]

  # get subscribed sync data
  cv_image=bridge.imgmsg_to_cv2(image,"bgr8")
  if CONFIG["visualization"]:
    vis_image=cv_image.copy()
  
  (rows,cols,channels) = cv_image.shape
  
  # prepare for publishing data
  out_img_global=np.zeros((rows,cols,channels))
  kps_list=KeypointsList()
  # sync for later use
  kps_list.header.stamp=image.header.stamp

  if len(boundingboxes.bounding_boxes) == 0:
    print("Ooops, nothing detected from Yolov3...")

  # for each bbx we found
  for item in boundingboxes.bounding_boxes:
    '''BoundingBox data format
    string Class
    float64 probability
    int64 xmin, xmax, ymin, ymax
    int64[] hm_keypoints
    float64[] img_keypoints 
    '''
    
    # kps msg copies boundingbox header and adding hm_keypoints and img_keypoints
    # hm_points (x,y)\in [0,63]X[0,63]
    # img_keypoints (x,y)\in [0,width]X[0,height]
    kps_item = Keypoints()
    kps_list.keypoints_list.append(kps_item)      
    kps_item.Class = item.Class
    kps_item.probability = item.probability
    kps_item.xmin = item.xmin
    kps_item.ymin = item.ymin
    kps_item.xmax = item.xmax
    kps_item.ymax = item.ymax
    kps_item.hm_keypoints = []
    kps_item.img_keypoints = []

    if CONFIG["visualization"]:
      cv2.rectangle(vis_image,(item.xmin,item.ymin),(item.xmax,item.ymax),(0,255,0),2)
      cv2.putText(vis_image,item.Class,(item.xmin,item.ymin-4),0,1,(0,0,255),2)

    # we only handle case when the class is in our dict
    if item.Class not in semantic_d:
      print("Detected %s~ no keypoints for it!"%(item.Class))
      #print("We only have [%s]"%(",".join([str(key) for key in semantic_d])))

    else:
      # we need to find the outer square range for this bbx and feed in the data
      ymin,ymax,xmin,xmax=item.ymin,item.ymax,item.xmin,item.xmax
      side=max(ymax-ymin,xmax-xmin)
      scale=side/255
      center_x=(xmax+xmin)/2
      center_y=(ymax+ymin)/2
      new_img=np.zeros((side,side,3))
      new_img[(side-ymax+ymin)//2:(side-ymin+ymax)//2,(side-xmax+xmin)//2:(side-xmin+xmax)//2,:]=cv_image[ymin:ymax,xmin:xmax,:]
      cropped_new_img=cv2.resize(new_img,(256,256),interpolation=cv2.INTER_CUBIC)

      # inference via stacked hourglass
      t_for_1=time.time()      
      heatmaps=sess.run(output_node, feed_dict={input_node:[cropped_new_img/255]})
      t_for_2=time.time()

      print("Class:%12s Prob:%.4f [xmin:%3d, xmax:%3d, ymin:%3d, ymax:%3d] infer:%4.2f ms"\
            %(item.Class,item.probability,item.xmin,item.xmax,item.ymin,item.ymax, 1000*(t_for_2-t_for_1)))

    # extract the keypoints location from heatmaps
    out_img_tmp=np.zeros((64,64,3))
    if item.Class in semantic_d:
      for j in semantic_d[item.Class]: # range(102):
        idx = np.argmax(heatmaps[0,:,:,j])
        hm_x=idx%64
        hm_y=idx//64
        img_x=min(max(int((hm_x-31.5)/63*255*scale+center_x),0),cols-1)
        img_y=min(max(int((hm_y-31.5)/63*255*scale+center_y),0),rows-1)
        out_img_tmp[hm_y,hm_x]=255
        out_img_global[img_y,img_x,:]=255
        kps_item.hm_keypoints.append(hm_x)
        kps_item.hm_keypoints.append(hm_y)
        kps_item.img_keypoints.append(img_x)
        kps_item.img_keypoints.append(img_y)
        
        window_ratio=np.sum(NonNeg(heatmaps[0,hm_y-3:hm_y+4,hm_x-3:hm_x+4,j]))/(np.sum(NonNeg(heatmaps[0,:,:,j]))+1e-14)
        inner_ratio=np.sum(NonNeg(heatmaps[0,hm_y-1:hm_y+2,hm_x-1:hm_x+2,j]))/(np.sum(NonNeg(heatmaps[0,hm_y-3:hm_y+4,hm_x-3:hm_x+4,j]))+1e-14)/0.4129

        kps_item.global_measures.append(window_ratio)
        kps_item.local_measures.append(inner_ratio)
        
        if CONFIG["visualization"]:
          cv2.circle(vis_image,(img_x,img_y), 5, (0,0,255), -1)
          cv2.putText(vis_image,str("G %.4f"%(window_ratio)),(img_x,img_y-4),0,0.2,(0,255,0),1)
          #cv2.putText(vis_image,str("L %.4f"%(inner_ratio)),(img_x,img_y-14),0,0.2,(0,255,255),1)
      print(kps_item.img_keypoints)#,kps_item.global_measures,kps_item.local_measures)

    out_img_tmp_list.append(out_img_tmp)

  return out_img_tmp_list, kps_list, out_img_global, vis_image

def NonNeg(matrix):
    newmat=np.array(matrix)
    newmat[newmat<0]=0
    return newmat

# callback function when receiving yolo bbx results
def callback_0(image, boundingboxes):
    t_start=time.time()
    print("left  receive",image.header.stamp.secs,image.header.stamp.nsecs)

    out_img_tmp_list, kps_list, out_img_global, vis_image = get_publish_data(image, boundingboxes)
    for out_img_tmp in out_img_tmp_list:
      hm_render_0.publish(bridge.cv2_to_imgmsg(out_img_tmp.astype(np.uint8),"bgr8"))

    # publish the KeypointsList information
    kps_pub_0.publish(kps_list)
    
    # publish the whole heatmaps(on image scale)
    img_render_0.publish(bridge.cv2_to_imgmsg(out_img_global.astype(np.uint8),"bgr8"))

    if CONFIG["visualization"]:
      vis_render_0.publish(bridge.cv2_to_imgmsg(vis_image.astype(np.uint8),"bgr8"))
    t_end=time.time()

    print("--------------------------")
    print("left  cycle total time %4.2f ms\n"%(1000*(t_end-t_start)))


# callback function when receiving yolo bbx results
def callback_1(image, boundingboxes):
    t_start=time.time()
    print("right receive",image.header.stamp.secs,image.header.stamp.nsecs)
    
    out_img_tmp_list, kps_list, out_img_global, vis_image = get_publish_data(image, boundingboxes)
    for out_img_tmp in out_img_tmp_list:
      hm_render_1.publish(bridge.cv2_to_imgmsg(out_img_tmp.astype(np.uint8),"bgr8"))

    # publish the KeypointsList information
    kps_pub_1.publish(kps_list)
    
    # publish the whole heatmaps(on image scale)
    img_render_1.publish(bridge.cv2_to_imgmsg(out_img_global.astype(np.uint8),"bgr8"))

    if CONFIG["visualization"]:
      vis_render_1.publish(bridge.cv2_to_imgmsg(vis_image.astype(np.uint8),"bgr8"))
      if CONFIG["save_to_file"]:
        cv2.imwrite(CONFIG["save_path"]+"/"+str(image.header.stamp.secs)+"."+str(image.header.stamp.nsecs)+".png",vis_image)
    t_end=time.time()

    print("--------------------------")
    print("right cycle total time %4.2f ms\n"%(1000*(t_end-t_start)))


# load the graph from pretrained model
def load_graph():

    # load the file and build the graph
    graph = tf.Graph().as_default()
    try:
        with tf.gfile.GFile(pwd+CONFIG["frozen_name"], "rb") as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())
    except:
        print("Failed to extract graphdef. Exiting..")
        quit()

    # fetch the input output nodes, as sess.run() placeholder
    input_node,output_node=tf.import_graph_def(graph_def, return_elements=[CONFIG["input_node_str"],CONFIG["output_node_str"]])
    
    # gpu setting
    gpu_options = tf.GPUOptions(allow_growth=True, force_gpu_compatible=True)
    config = tf.ConfigProto(allow_soft_placement=True,log_device_placement=False, gpu_options=gpu_options)
    config.graph_options.optimizer_options.global_jit_level = tf.OptimizerOptions.ON_2
    
    # enable the session
    sess= tf.Session(config=config)

    return input_node,output_node,sess


if __name__ == '__main__':
    # load config
    with open(pwd+'config.yaml') as f:
      CONFIG=yaml.safe_load(f)

    # load the graph
    input_node, output_node, sess = load_graph()
    
    # active the bridge
    bridge = CvBridge()
    rospy.init_node('kp_detector')
    
    # define the publishers
    kps_pub_0 = rospy.Publisher(CONFIG["kps_topic_0"], KeypointsList, queue_size=100)
    hm_render_0 = rospy.Publisher(CONFIG["hm_topic_0"], Image, queue_size=100)
    img_render_0 = rospy.Publisher(CONFIG["hm_img_topic_0"],Image, queue_size=100)
    vis_render_0 = rospy.Publisher(CONFIG["vis_topic_0"],Image,queue_size=100)

    kps_pub_1 = rospy.Publisher(CONFIG["kps_topic_1"], KeypointsList, queue_size=100)
    hm_render_1 = rospy.Publisher(CONFIG["hm_topic_1"], Image, queue_size=100)
    img_render_1 = rospy.Publisher(CONFIG["hm_img_topic_1"],Image, queue_size=100)
    vis_render_1 = rospy.Publisher(CONFIG["vis_topic_1"],Image,queue_size=100)

    # define the sync subscriber(google `message filter` for more info)
    tss_0 = TimeSynchronizer([Subscriber(CONFIG["image_src_0"], Image),
                              Subscriber(CONFIG["bbxes_src_0"], BoundingBoxes)],
                             200)
    tss_0.registerCallback(callback_0)

    tss_1 = TimeSynchronizer([Subscriber(CONFIG["image_src_1"], Image),
                           Subscriber(CONFIG["bbxes_src_1"], BoundingBoxes)],200)
    tss_1.registerCallback(callback_1)
    rospy.spin()

