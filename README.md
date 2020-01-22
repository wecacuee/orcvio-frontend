# Run frontend for OrcVIO

1. Download weights for darknet by following instructions [here](src/darknet_ros/darknet_ros/yolo_network_config/weights/how_to_download_weights.txt). By default the weights used are `./src/darknet_ros/darknet_ros/yolo_network_config/weights/yolov2-tiny.weights`

2. Download weights for kp_detector from 
[here](https://drive.google.com/open?id=1VxinRLP1RBRjlHUkyFoDBfNqLfgs_zG_). Put the weights as `./src/kp_detector/frozen_nhwc.pb`

3. Build the docker image

  ``` shellsession
  docker build -t orcvio .
  ```

4. Run the docker image

  ``` shellsession
  docker-compose up starmap_kp
  ```

