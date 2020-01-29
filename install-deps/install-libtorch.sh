wget https://download.pytorch.org/libtorch/cu101/libtorch-cxx11-abi-shared-with-deps-1.4.0.zip -O /tmp/libtorch-cxx11-abi-shared-with-deps-1.4.0.zip
mkdir -p $CATKIN_WORKSPACE/devel/ && \
unzip /tmp/libtorch-cxx11-abi-shared-with-deps-1.4.0.zip -d $CATKIN_WORKSPACE/devel/
rsync -arP $CATKIN_WORKSPACE/devel/libtorch/ $CATKIN_WORKSPACE/devel/
