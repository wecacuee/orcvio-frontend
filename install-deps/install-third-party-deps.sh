
# Install vision_opencv and open_vins
{
mkdir -p $CATKIN_WORKSPACE/src && cd $CATKIN_WORKSPACE && \
    git clone https://github.com/ros-perception/vision_opencv.git src/vision_opencv && \
    git clone https://github.com/rpng/open_vins/ src/open_vins && \
    . /opt/ros/melodic/setup.sh && \
    catkin config -DPYTHON_EXECUTABLE=/usr/bin/python3 -DPYTHON_INCLUDE_DIR=/usr/include/python3.6m -DPYTHON_LIBRARY=/usr/lib/x86_64-linux-gnu/libpython3.6m.so && \
    catkin build
}
