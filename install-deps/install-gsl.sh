#mkdir -p $CATKIN_WORKSPACE/devel/include/gsl/
#wget https://github.com/gsl-lite/gsl-lite/blob/master/include/gsl/gsl-lite.hpp -O $CATKIN_WORKSPACE/devel/include/gsl/gsl-lite.hpp
{
git clone --branch v0.36.0 https://github.com/gsl-lite/gsl-lite.git /tmp/gsl-lite  && \
    cd /tmp/gsl-lite && \
    cmake -H. -Bbuild -DCMAKE_INSTALL_PREFIX=$CATKIN_WORKSPACE/devel && \
    cmake --build build --target install;
}

