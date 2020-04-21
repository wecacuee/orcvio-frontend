URL=https://download.pytorch.org/libtorch/cu101/libtorch-cxx11-abi-shared-with-deps-1.4.0.zip
SOURCE_PREFIX=${HOME}/.local/src
STOW_PREFIX=${SOURCE_PREFIX}/stow
if [ ! -f "${STOW_PREFIX}/libtorch-1.4.0/share/cmake/Torch/TorchConfig.cmake" ]; then
    wget $URL -O ${SOURCE_PREFIX}/libtorch-cxx11-abi-shared-with-deps-1.4.0.zip
    mkdir -p $STOW_PREFIX && \
        unzip ${SOURCE_PREFIX}/libtorch-cxx11-abi-shared-with-deps-1.4.0.zip -d $STOW_PREFIX
    mv $STOW_PREFIX/libtorch $STOW_PREFIX/libtorch-1.4.0
fi

stow --dir=${STOW_PREFIX} --target=$INSTALL_PREFIX libtorch-1.4.0
