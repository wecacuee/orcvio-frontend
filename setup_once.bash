sudo sh install-deps/install-apt-get-packages.sh

pip3 install --no-cache -r install-deps/pip-requirements.txt

{
    export CATKIN_WORKSPACE=$(pwd)
    export SUDO=sudo
    [ -d $CATKIN_WORKSPACE/devel/share/OpenCV/ ] || \
        sh install-deps/install-opencv.sh
    [ -d $CATKIN_WORKSPACE/devel/lib/libtorch.so ] || \
        sh install-deps/install-libtorch.sh
    [ -d $CATKIN_WORKSPACE/src/vision_opencv ] || \
        sh install-deps/clone-deps-and-catkin-build.sh
    [ -f $CATKIN_WORKSPACE/devel/include/gsl-lite/gsl-lite.hpp ] || \
        sh install-deps/install-gsl.sh
    [ -f $CATKIN_WORKSPACE/src/darknet_ros/darknet_ros/yolo_network_config/weights/yolov2.weights ] || \
        sh install-deps/download-yolo-weights.sh
}

