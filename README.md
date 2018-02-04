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

Datasets with pedestrians:
1. KITTI

    Among lot of various road environment datasets there are two which are useful    for our problem:
    * [Dataset for detection](http://www.cvlibs.net/datasets/kitti/eval_object.php?obj_benchmark=2d) 
    with 8 classes (Car, Van, Truck, Pedestrian, Person_sitting, Cyclist, Tram, Misc).
    * [Dataset for object tracking](http://www.cvlibs.net/datasets/kitti/eval_tracking.php) with the same 8 classes. 

        
2. Cityscapes

    Road scene [segmentation dataset](https://www.cityscapes-dataset.com/). Labels are provided as masks for classes of objects and object`s instances. 

3. Daimler

    There are [road environment datasets](http://www.gavrila.net/Datasets/datasets.html) for different problems:
    * Pedestrian segmentation
    * Pedestrian path prediction (stopping, crossing, bending in, starting)
    * Stereo pedestrian detection
    * Mono pedestrian detection (this should be taken)
    * Mono pedestrian classification
    * Cyclists detection

4. Caltech
 
    > [The Caltech Pedestrian Dataset](http://www.vision.caltech.edu/Image_Datasets/CaltechPedestrians/) consists of approximately 10 hours of 640x480 30Hz video taken from a vehicle driving through regular traffic in an urban environment. About 250,000 frames (in 137 approximately minute long segments) with a total of 350,000 bounding boxes and 2300 unique pedestrians were annotated.

5. MOT17 (Multiple Object Tracking Benchmark)
    
    [Dataset](https://motchallenge.net/data/MOT17Det) for multiple object tracking mostly related to pedestrian tracking.

6. KAIST

    > [The KAIST Multispectral Pedestrian Dataset](https://sites.google.com/site/pedestrianbenchmark/) consists of 95k color-thermal pairs (640x480, 20Hz) taken from a vehicle. All the pairs are manually annotated (person, people, cyclist) for the total of 103,128 dense annotations and 1,182 unique pedestrians. The annotation includes temporal correspondence between bounding boxes like Caltech Pedestrian Dataset.

7. Oxford RobotCar Dataset

    [Dataset](http://robotcar-dataset.robots.ox.ac.uk/) was collected in over 1000 km of recordered driving in all weather conditions. There are almost 20 million images of the same road from 6 cameras.


### 2. Evaluation of datasets
With a first "human" evaluation we concluded that:
1. KITTI is a useful dataset, rich of detected pictures with well-made labels
2. Cityscapes is a segmentation dataset and it'll require a lot of work to convert segmentation labels to bounding boxes for detection, so we have decided to drop it
3. Daimler has only black & white pictures so we have decided to drop it
4. Caltech: Ruslan is working on it
5. MOT-17 TO DO
6. KAIST TO DO
7. Oxford is too big to be evaluated with our personal machines so we have decided to drop it
