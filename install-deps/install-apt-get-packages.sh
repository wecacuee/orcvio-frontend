echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list
apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654

apt-get update && \
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
            rsync \
            unzip \
    && \
    rm -rf /var/lib/apt/lists/*
