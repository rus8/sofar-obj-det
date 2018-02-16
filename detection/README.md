# CNN for detection

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