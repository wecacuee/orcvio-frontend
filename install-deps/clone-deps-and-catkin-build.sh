
# Install vision_opencv and open_vins
{
mkdir -p $CATKIN_WORKSPACE/src; cd $CATKIN_WORKSPACE && \
    . /opt/ros/melodic/setup.sh && \
    catkin config -DPYTHON_EXECUTABLE=/usr/bin/python3 -DPYTHON_INCLUDE_DIR=/usr/include/python3.6m -DPYTHON_LIBRARY=/usr/lib/x86_64-linux-gnu/libpython3.6m.so && \
    cd src && wstool init ; \
        rosinstall_generator image_pipeline rosbag vision_opencv | wstool merge - && \
    cd -
    catkin build
}
