# MOT17 Dataset
The main interest of the authors of the dataset is to track moving objects in videos. In particular, they are interested in multiple people tracking algorithms, therefore, people will be the center of attention.
They provide a set of 600 pictures with a labels file.
A detailed description of dataset and relative benchmarks can be found [here](https://arxiv.org/pdf/1603.00831.pdf).

## Labels description:
Detection and annotation files are simple comma-separated value (CSV) files. Each line represents one object instance and contains 9 values as shown in the following table.

| Position | Name | Description |
|:------:|:-----:|:----------|
| 1 | Frame number | Indicate at which frame the object is present |
| 2 | Identity number | Each pedestrian trajectory is identified by a unique ID (−1 for detections) |
| 3 | Bounding box left | Coordinate x of the top-left corner of the pedestrian bounding box |
| 4 | Bounding box top | Coordinate y of the top-left corner of the pedestrian bounding box |
| 5 | Bounding box width | Width in pixels of the pedestrian bounding box | 
| 6 | Bounding box height | Height in pixels of the pedestrian bounding box |
| 7 | Confidence score | It acts as a flag whether the entry is to be considered (1) or ignored (0). |
| 8 | Class | Indicates the type of object annotated |
| 9 | Visibility | Visibility ratio, a number between 0 and 1 that says how much of that object is visible. Can be due to occlusion and due to image border cropping. |

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