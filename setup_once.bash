sudo sh install-deps/install-apt-get-packages.sh

{
    export CATKIN_WORKSPACE=$(pwd)
    export INSTALL_PREFIX=${CATKIN_WORKSPACE}/devel
    export SUDO=sudo
    [ -d $INSTALL_PREFIX/lib/libtorch.so ] || \
        sh install-deps/install-libtorch.sh
    [ -f $CATKIN_WORKSPACE/src/backend/src/darknet_ros/darknet_ros/yolo_network_config/weights/yolov2.weights ] || \
        sh install-deps/download-yolo-weights.sh
    [ -f $INSTALL_PREFIX/include/sophus/se3.hpp ] || \
        make -f install-deps/install-sophus.mk
    [ -f $INSTALL_PREFIX/share/catkin_simple/cmake/catkin_simpleConfig.cmake ] || \
        make -f install-deps/install-catkin-simple.mk
}

virtualenv --python=python3.6 .tox/py36
source .tox/py36/bin/activate
pip3 install --no-cache -r install-deps/pip-requirements.txt
{
    export CATKIN_WORKSPACE=$(pwd)
    [ -d $CATKIN_WORKSPACE/src/vision_opencv ] || \
        sh install-deps/clone-deps-and-catkin-build.sh

}
catkin config --extend /opt/ros/melodic/setup.bash
catkin build
source setup.bash

