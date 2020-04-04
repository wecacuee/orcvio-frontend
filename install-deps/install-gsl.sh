#mkdir -p $CATKIN_WORKSPACE/devel/include/gsl/
#wget https://github.com/gsl-lite/gsl-lite/blob/master/include/gsl/gsl-lite.hpp -O $CATKIN_WORKSPACE/devel/include/gsl/gsl-lite.hpp
{
    SOURCE_PREFIX=$HOME/.local/src
    STOW_PREFIX=$SOURCE_PREFIX/stow
git clone --branch v0.36.0 https://github.com/gsl-lite/gsl-lite.git $SOURCE_PREFIX/gsl-lite  && \
    cd $SOURCE_PREFIX/gsl-lite && \
    cmake -H. -Bbuild -DCMAKE_INSTALL_PREFIX=$STOW_PREFIX/gsl-0.36.0 && \
    cmake --build build --target install && \
    stow --dir=$STOW_PREFIX --target=$INSTALL_PREFIX gsl-0.36.0
}

