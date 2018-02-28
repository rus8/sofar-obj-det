# CNN for detection
Training is performed via Darkflow library. For detection there are two approaches presented:
via Darkflow and via pure TensorFlow.

## Inference via Darkflow
Running existing detectors is pretty straight forward. One could follow
instructions in Darkflow repository. 

To provide examples we wrote 
scripts: `detection/cam_inferance.py` and `detection/img_inference.py`.  
To run them one should download from Darknet website [weights](https://pjreddie.com/media/files/tiny-yolo-voc.weights`) 
of TinyYOLO network trained on PASCAL VOC dataset.

## Inference via "objdet" package (pure TensorFlow)


## Training the detector
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
 
 To establish training pipeline via Darkflow we selected Caltech dataset
 (as it is easy to add data from KAIST dataset so together they will 
 combine really huge dataset) and wrote a script `data-eval/caltech2yolo.py`
 to  prepare it according to Darknet format for pedestrian 
 ("person" label) detection. It is also required to apply patch 
 `Train_on_Caltech.patch` from the root folder of the repository before
 installing Darkflow. This process is described in `dev-env.md`.
 
 Also some changes in configuration are required. In Darkflow directory
 file `labels.txt` should contain only one word: `person`. And you have to 
 copy in you`darkflow/cfg` folder network configuration file `tiny-yolo-pedect.cfg`
 from the root of this repository. 
 
 After all preparations you could train a new model with command 
 (from Darkflow directory):  
 `flow --model cfg/tiny-yolo-pedect.cfg --train --annotation "/home/rr/Desktop/Caltech_ped_det/part/labels/" --dataset "/home/rr/Desktop/Caltech_ped_det/part/frames/"`
 
 Darkflow also allows to perform transfer learning, so you could use
 weights of already trained network. For this you could download
 weights from Darknet website and put them in your `darkflow/bin` 
 folder. Darkflow will automatically define what layers are the same
 comparing with configuration file with the same name as weights file.
 For example for our problem one could do like this:  
 `flow --model cfg/tiny-yolo-pedect.cfg --load bin/tiny-yolo-voc.weights --train --annotation "/home/rr/Desktop/Caltech_ped_det/part/labels/" --dataset "/home/rr/Desktop/Caltech_ped_det/part/frames/"`