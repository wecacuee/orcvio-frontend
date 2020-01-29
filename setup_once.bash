sudo sh install-deps/install-apt-get-packages.sh

pip3 install --no-cache -r install-deps/pip-requirements.txt

CATKIN_WORKSPACE=$(pwd) SUDO=sudo sh install-deps/install-third-party-deps.sh
CATKIN_WORKSPACE=$(pwd) SUDO=sudo sh install-deps/install-opencv.sh
CATKIN_WORKSPACE=$(pwd) SUDO=sudo sh install-deps/install-libtorch.sh

# Download weights
{
    cd src/darknet_ros/darknet_ros/yolo_network_config/weights/
    curl -OJL http://pjreddie.com/media/files/yolov2.weights
    curl -OJL http://pjreddie.com/media/files/yolov2-tiny.weights
    curl -OJL http://pjreddie.com/media/files/yolov2-voc.weights
    curl -OJL http://pjreddie.com/media/files/yolov2-tiny-voc.weights
    curl -OJL http://pjreddie.com/media/files/yolov3-voc.weights
    curl -OJL http://pjreddie.com/media/files/yolov3.weights
} ; cd -
