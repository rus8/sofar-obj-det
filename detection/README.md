# CNN for detection

## YOLO architecture

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
project we have tpo use TensorFlow so we looked on the internet and found
implementation [darkflow](https://github.com/thtrieu/darkflow),
which allows to easily use YOLO in TensorFlow. It allows to try 
architecture without CUDA Toolkit using only CPU version of TensorFlow, 
however it requires installation which includes compilation of some
Cython functions which are required for YOLO to make it faster.

## Running existing detectors

## Training our detector
According to the guide on the [official website](https://pjreddie.com/darknet/yolo/)
it's required to prepare dataset in the following way:
 * Images folder of each part of dataset, and corresponding labels folder
  should be inside one directory. Each label file should have the name of corresponding image file but 
 with ".txt" extension.  
 └── dataset  
 &nbsp;&nbsp;&nbsp;&nbsp;├── part1  
 &nbsp;&nbsp;&nbsp;&nbsp;│   ├── images  
 &nbsp;&nbsp;&nbsp;&nbsp;│   │   └── img0001.jpg  
 &nbsp;&nbsp;&nbsp;&nbsp;│   └── labels  
 &nbsp;&nbsp;&nbsp;&nbsp;│    &nbsp;&nbsp;&nbsp;&nbsp; └── img0001.txt  
 &nbsp;&nbsp;&nbsp;&nbsp;└── part2  
 &nbsp;&nbsp;&nbsp;&nbsp; . . .
 
 * In the label file there should be a line for each labeled object in the
 format:  
 `<object-class> <x> <y> <width> <height>`  
 where `<object-class>` is the serial number of the class among considered
 classes, `<x> <y>` are coordinates of top left corner of the bounding box, 
 `<width> <height>` are sizes of the bounding box. The latter four should be
 presented relatively to image sizes (in interval `[0; 1]`).