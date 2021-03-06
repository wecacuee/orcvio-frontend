# Download weights
{
    cd ${CATKIN_WORKSPACE}/src/backend/src/darknet_ros/darknet_ros/yolo_network_config/weights/
    [ -f yolov2.weights ] || \
        curl -OJL http://pjreddie.com/media/files/yolov2.weights
    [ -f yolov2-tiny.weights ] || \
        curl -OJL http://pjreddie.com/media/files/yolov2-tiny.weights
    [ -f yolov2-voc.weights ] || \
        curl -OJL http://pjreddie.com/media/files/yolov2-voc.weights
    [ -f yolov2-tiny-voc.weights ] || \
        curl -OJL http://pjreddie.com/media/files/yolov2-tiny-voc.weights
    [ -f yolov3-voc.weights ] || \
        curl -OJL http://pjreddie.com/media/files/yolov3-voc.weights
    [ -f yolov3.weights ] || \
        curl -OJL http://pjreddie.com/media/files/yolov3.weights
} ; cd -
