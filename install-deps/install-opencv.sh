# Install opencv
{
    mkdir -p /tmp/opencv_build && \
        cd /tmp/opencv_build && \
        git clone --branch 3.4.6 https://github.com/opencv/opencv/ && \
        git clone --branch 3.4.6 https://github.com/opencv/opencv_contrib/ && \
        mkdir opencv/build/ && \
        cd opencv/build/ && \
        cmake -DOPENCV_EXTRA_MODULES_PATH=../../opencv_contrib/modules .. && \
        make -j && \
        $SUDO make install && \
        cd && rm -rf /home/root/opencv_build
}
