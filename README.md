# SofAR Obstacle detection project 

### Team
* Ruslan Aminev
* Luigi Secondo

### Project plan

1. Find datasets
2. Evaluate datasets, select feasible one
3. Choose detection algorithm (DNN architecture)
4. Prepare labels according to chosen algorithm
5. Develop training pipeline and train neural network
6. Integrate algorithm in ROS
___

### 1. Find datasets
Suitable dataset should contain images or image sequences of scenes, 
where different number of persons could be present. Labels should 
determine position of the person on the image in terms
of the bounding box (or should be convertible to bounding box).

Datasets with pedestrians:
1. KITTI

    Among lot of various road environment datasets there is one 
    which is useful for our problem:
    * [Dataset for detection](http://www.cvlibs.net/datasets/kitti/eval_object.php?obj_benchmark=2d) 
    with 8 classes (Car, Van, Truck, Pedestrian, Person_sitting, Cyclist, Tram, Misc).

        
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

___

### 2. Evaluation of datasets
With a first "human" evaluation we concluded that:
1. KITTI is not very large but could be useful, so we evaluate it. 
2. Cityscapes is a segmentation dataset and it'll require a lot 
of work to convert segmentation labels to bounding boxes for detection, 
so we have decided to drop it.
3. Daimler has only black & white pictures, so we have decided to drop it.
4. Caltech was created specifically for our problem and has a lot of
images, so we evaluate it.
5. MOT-17 was also created for pedestrians detection, so we evaluate it.
6. KAIST is compatible with Caltech in terms of labels and has a lot of images, so we 
evaluate it.
7. Oxford is too big to be evaluated with our personal machines so we have decided to drop it

For a more detailed report for each evaluated dataset (1, 4, 5, 6) 
check `README.md` in `data-eval` folder.
___

### 3. Choose detection algorithm

There are several well known object detection approaches which use CNN
as their main part: Fast RCNN, Faster RCNN, SSD, YOLO, and others.

For our problem we selected [YOLO](https://arxiv.org/abs/1506.02640) 
(there also exists the [second version](https://arxiv.org/abs/1612.08242)) as it has ability to simultaneously
detect (in one pass) and classify object in image. SSD architecture also has this
property, but choice of YOLO was also dictated by presence of really
light version of architecture "Tiny YOLO". It should be able to perform in real
time pace on low grade hardware like mobile versions of NVIDIA GPUs in
laptops or [NVIDIA Jetson TX](https://www.nvidia.com/en-us/autonomous-machines/embedded-systems-dev-kits-modules/)
modules. However, Tiny YOLO has worse accuracy than full size network.

Authors of YOLO provide their implementation in pure C and CUDA called 
[Darknet](https://pjreddie.com/darknet/). It requires compilation from 
source and presence of CUDA Toolkit. According to requirements of the 
project we have to use TensorFlow so we looked on the internet and found
implementation [darkflow](https://github.com/thtrieu/darkflow),
which allows to easily use YOLO in TensorFlow. It allows to try 
architecture without CUDA Toolkit using only CPU version of TensorFlow, 
however it requires installation which includes compilation of some
Cython functions which are required for YOLO to make it faster.

We are able to run existing detectors for several classes, 
which are trained on [VOC](http://host.robots.ox.ac.uk/pascal/VOC/)
or [COCO](http://cocodataset.org/#home) datasets with "person" class
among others (see `detection/cam_inference.py` and 
`detection/img_inference.py`). To perform this darkflow is used 
according the instructions in it's repository.

___

### 4. Prepare labels

Darkflow is said to be TensorFlow implementation of Darknet, however 
it's internal label parsing tools for training are not designed according to Darknet
conventions, which are described on Darknet website.

So to use Darkflow for training with your own dataset it's required to 
change some code to use labels formatted according to Darknet 
well defined rules. In our case a patch was written.

The whole process is described in more details in `detection/README.md`.
___

### 5. Training

If the dataset and network configuration are prepared properly training
is easy, one just have to use Darkflow command to do it:  
`flow --model cfg/tiny-yolo-voc-3c.cfg --load bin/tiny-yolo-voc.weights 
--train --annotation train/Annotations --dataset train/Images`

For more details also look in `README.md` in `detection` folder.

Unfortunately there were no proper hardware available for training,
but there are some possibilities to use online services:
1. [Amazon Web Services](https://aws.amazon.com/) 
(some credits are available via
[GitHub Student Developer Pack](https://education.github.com/pack)).
2. [Google Cloud Platform](https://cloud.google.com) with 300$ free credits.
3. [Google Colaboratory](https://colab.research.google.com/notebooks/welcome.ipynb) 
with totally free access to machines with NVIDIA Tesla K80 13Gb.

However understanding and configuration of this tools require a lot of 
time compared with straightforward training using local machine. So
for now we don't provide our trained neural network specifically for 
the problem of pedestrian detection, but developed workflow allows 
to easily do this.
___

### 6. Integrate algorithm in ROS
In order to run detection in ROS environment we create a ROS 
Detection node which is able to read images from any appropriate topic.
It runs detection and publishes results in ROS to make them available 
for other nodes.

![scheme](uml-scheme.png)

To use OpenCV for image related operations  we have to convert them to 
OpenCV format using CvBridge which is a ROS library with required functions.


___

### Conclusion

- 
- check compatability of libraries
- look for available architectures before evaluating datasets