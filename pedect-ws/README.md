# ROS integration
Here is workspace which contains "obj_detector" package based on 
"objdet" package. This package defines special custom message for 
publishing detection results, and provides example node for detection.


## Environment

Install main dependencies:
```
$ pip install cython pyaml numpy tensorflow==1.0
```

Install "objdet" package provided in this project:
```
$ cd detection
$ pip install .
```