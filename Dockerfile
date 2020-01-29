FROM nvidia/cuda:10.1-cudnn7-devel-ubuntu18.04 AS cuda

ENV TZ=America/Los_Angeles
ENV DEBIAN_FRONTEND=noninteractive

COPY install-deps/install-apt-get-packages.sh /tmp/
RUN sh /tmp/install-apt-get-packages.sh

COPY install-deps/pip-requirements.txt /tmp/
RUN pip3 install --no-cache -r /tmp/pip-requirements.txt

COPY install-deps/install-opencv.sh /tmp/
RUN CATKIN_WORKSPACE=/home/root/catkin_ws SUDO="" sh /tmp/install-opencv.sh

COPY install-deps/install-third-party-deps.sh /tmp/
RUN CATKIN_WORKSPACE=/home/root/catkin_ws SUDO="" sh /tmp/install-third-party-deps.sh

COPY install-deps/install-libtorch.sh /tmp/
RUN CATKIN_WORKSPACE=/home/root/catkin_ws SUDO="" sh /tmp/install-libtorch.sh

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
