FROM nvidia/cuda:10.1-cudnn7-devel-ubuntu18.04 AS cuda

ENV TZ=America/Los_Angeles
ENV DEBIAN_FRONTEND=noninteractive

RUN echo "deb http://packages.ros.org/ros/ubuntu bionic main" > /etc/apt/sources.list.d/ros-latest.list
RUN apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654

RUN apt-get update && \
    apt-get -y install python3-pip git \
                       ros-melodic-tf-conversions \
                       ros-melodic-random-numbers \
                       libsuitesparse-dev \
                       ros-melodic-pluginlib \
                       ros-melodic-opencv-apps \
                       ros-melodic-pcl-conversions \
                       ros-melodic-rviz \
                      ros-melodic-ros-base \
                      ros-melodic-eigen-conversions \
                      ros-melodic-pcl-ros \
                       libsm-dev \
                       libxrender-dev \
    && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache catkin-tools rospkg rosdistro opencv-python matplotlib tensorflow==1.6 empy

RUN mkdir -p /home/root/catkin_ws/src && cd /home/root/catkin_ws && \
    git clone https://github.com/ros-perception/vision_opencv.git src/vision_opencv && \
    . /opt/ros/melodic/setup.sh && \
    catkin config -DPYTHON_EXECUTABLE=/usr/bin/python3 -DPYTHON_INCLUDE_DIR=/usr/include/python3.6m -DPYTHON_LIBRARY=/usr/lib/x86_64-linux-gnu/libpython3.6m.so && \
    catkin build

# ROS Python 3 fix
RUN sed -i -e 's/import itertools/import itertools\nfrom functools import reduce/' /opt/ros/melodic/lib/python2.7/dist-packages/message_filters/__init__.py

RUN echo '#!/bin/bash\n\
set -e\n\
\n\
source /opt/ros/melodic/setup.bash || true\n\
source /home/root/catkin_ws/devel/setup.bash || true\n\
exec "$@"\n\
' > /ros_entrypoint.bash
RUN chmod +x /ros_entrypoint.bash
ENTRYPOINT ["/ros_entrypoint.bash"]
