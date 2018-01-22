# Kitty Dataset
Among lot of various road environment datasets there are two which are useful    for our problem:
* [Dataset for detection](http://www.cvlibs.net/datasets/kitti/eval_object.php?obj_benchmark=2d) 
with 8 classes (Car, Van, Truck, Pedestrian, Person_sitting, Cyclist, Tram, Misc).
* [Dataset for object tracking](http://www.cvlibs.net/datasets/kitti/eval_tracking.php) with the same 8 classes. 

It provides several pictures with corresponding labels files to train the network and many other pictures to test the training (see folder "Detection").

## Labels description:

| Values | Name | Description |
|:------:|:-----:|:----------|
| 1 | type | Describes the type of object: 'Car', 'Van', 'Truck', 'Pedestrian', 'Person_sitting', 'Cyclist', 'Tram', 'Misc' or 'DontCare'|
| 1 | truncated | Float from 0 (non-truncated) to 1 (truncated), where truncated refers to the object leaving image boundaries |
| 1 | Occulted | Integer (0,1,2,3) indicating occlusion state: 0 = fully visible, 1 = partly occluded 2 = largely occluded, 3 = unknown |
| 1 | alpha | Observation angle of object, ranging [-pi..pi] |
| 4 | bbox | 2D bounding box of object in the image (0-based index): contains left, top, right, bottom pixel coordinates | 
| 3 | dimentions | 3D object dimensions: height, width, length (in meters) |
| 3| location | 3D object location x,y,z in camera coordinates (in meters) |
| 1 | rotation_y | Rotation ry around Y-axis in camera coordinates [-pi..pi] |
| 1 | score | Only for results: Float, indicating confidence in detection, needed for p/r curves, higher is better. |
        