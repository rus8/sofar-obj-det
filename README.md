# SofAR Obstacle detection project 

### Team
* Luigi Secondo
* Ruslan Aminev

### Plan draft

1. Find datasets
2. Evaluate datasets, select feasible one
3. Choose detection algorithm (DNN architecture)
4. Prepare labels according to chosen algorithm
5. Evaluate the perfomance of the algorithm
6. Integrate algorithm in ROS
7. Apply algorithm to real robot (Husqvarna)

### Possible enhancements

* Combine several datasets in one


### 1. Find datasets
Suitable dataset should contain images or image sequences of scenes, where different number
of persons could present. Labels should determine position of the person on the image in terms
of the bounding box (or should be convertible to bounding box).

