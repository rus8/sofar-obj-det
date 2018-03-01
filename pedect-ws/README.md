# ROS integration
Here is workspace which contains "obj_detector" ROS package based on 
"objdet" Python package. This package defines special custom message for 
publishing detection results, and provides example node for detection.

Also there are two other packages ("cam_pub" and "detection_consumer")
which together with "obj_detector" combine the example of using detection in ROS.

## Custom msg
To publish detection results we have defined custom message 
`DetectedBoxes.msg` which is defined as
 ```
 Header header
string dictionary
```

Where `header` should be copied from Image message for which detection is 
performed. This allows to synchronize topics for final user of 
the detection results.

## Environment
To run examples contained in this workspace it's required to:

1. Install main dependencies:
```
$ pip install cython pyaml numpy tensorflow==1.0
```

2. Install "objdet" package provided in this project:
```
$ cd detection
$ pip install .
```