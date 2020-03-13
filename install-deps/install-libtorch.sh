URL=https://download.pytorch.org/libtorch/cu101/libtorch-cxx11-abi-shared-with-deps-1.4.0.zip
wget $URL -O /tmp/libtorch-cxx11-abi-shared-with-deps-1.4.0.zip
mkdir -p $CATKIN_WORKSPACE/devel/stow/ && \
unzip /tmp/libtorch-cxx11-abi-shared-with-deps-1.4.0.zip -d $CATKIN_WORKSPACE/devel/stow/
cd $CATKIN_WORKSPACE/devel/stow && stow libtorch
