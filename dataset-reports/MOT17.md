# MOT17 Dataset
The main interest of the authors of the dataset is to track moving objects in videos. In particular, they are interested in multiple people tracking algorithms, therefore, people will be the center of attention.
They provide a set of 600 pictures with a labels file.
A detailed description of dataset and relative benchmarks can be found [here](https://arxiv.org/pdf/1603.00831.pdf).

![alt text](MOT17.jpg)
## Labels description:
Detection and annotation files are simple comma-separated value (CSV) files. Each line represents one object instance and contains 9 values as shown in the following table.

| Position | Name | Description |
|:------:|:-----:|:----------|
| 0 | Frame number | Indicate at which frame the object is present |
| 1 | Identity number | Each pedestrian trajectory is identified by a unique ID (−1 for detections) |
| 2 | Bounding box left | Coordinate x of the top-left corner of the pedestrian bounding box |
| 3 | Bounding box top | Coordinate y of the top-left corner of the pedestrian bounding box |
| 4 | Bounding box width | Width in pixels of the pedestrian bounding box | 
| 5 | Bounding box height | Height in pixels of the pedestrian bounding box |
| 6 | Confidence score | It acts as a flag whether the entry is to be considered (1) or ignored (0). |
| 7 | Class | Indicates the type of object annotated |
| 8 | Visibility | Visibility ratio, a number between 0 and 1 that says how much of that object is visible. Can be due to occlusion and due to image border cropping. |

Classes of detected objects and their corresponding values:

| ID | Class |
|:-----:|:------:|
| 1 | Pedestrian |
| 2 | Person on vehicle|
| 3 | Car |
| 4 | Bicycle |
| 5 | Motorcycle |
| 6 | Non motorized vehicle |
| 7 | Static person |
| 8 | Distractor |
| 9 | Occluder |
| 10 | Occluder on the ground |
| 11 | Occluder full |
| 12 | Reflection |

If a person is cropped by the image border, the box is estimated beyond the original frame to represent the entire person and to estimate the level of cropping.
As you can see, the dataset also distinguishes people inside vehicles.
For our purpose we decided to drop pictures with people inside vehicles to not create ambiguities in the neural network training and we cropped bounding boxes which were not completely included in the picture.

## Evaluation results

Total number of pictures:  600 \
Total number of pedestrians:  18581 \
Total number of pictures with pedestrians: 600 \
Total number of pictures without pedestrians:  0 \
Average of pedestrians per picture with pedestrians:  30.9683 \
Average of pedestrians per picture in general:  30.9683 