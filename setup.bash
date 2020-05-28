DIR=$(dirname $(readlink -m ${BASH_SOURCE[0]}))
#source /opt/ros/melodic/setup.bash
export CMAKE_PREFIX_PATH=${HOME}/aux/orcvio-frontend/devel:$CMAKE_PREFIX_PATH
export PYTHONPATH=${HOME}/aux/orcvio-frontend/devel/lib/python3.6/dist-packages:$PYTHONPATH

export ROS_PYTHON_VERSION=3
export PYTHONPATH=$PYTHONPATH:/opt/ros/melodic/lib/python2.7/dist-packages
#export PYTHONPATH=/usr/lib/python3/dist-packages/:$PYTHONPATH
#export PYTHONPATH=/usr/local/lib/python3.6/dist-packages:$PYTHONPATH
export DATA_DIR=$HOME/dataset
source ${DIR}/.tox/py3?/bin/activate
[ -f $DIR/devel/setup.bash ] && source $DIR/devel/setup.bash
