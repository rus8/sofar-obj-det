# MOT17 Dataset
The main interest of the authors of the dataset is to track moving objects in videos. In particular, they are interested in multiple people tracking algorithms, therefore, people will be the center of attention.
They provide a set of 600 pictures with a labels file.

## Labels description:
Detection and annotation files are simple comma-separated value (CSV) files. Each line represents one object instance and contains 9 values as shown in the following table.

| Position | Name | Description |
|:------:|:-----:|:----------|
| 1 | Frame number | Indicate at which frame the object is present |
| 2 | Identity number | Each pedestrian trajectory is identified by a unique ID (−1 for detections) |
| 3 | Bounding box left | Coordinate of the top-left corner of the pedestrian bounding box |
| 4 | Bounding box top | Coordinate of the top-left corner of the pedestrian bounding box |
| 5 | Bounding box width | Width in pixels of the pedestrian bounding box | 
| 6 | Bounding box height | Height in pixels of the pedestrian bounding box |
| 7 | Confidence score | It acts as a flag whether the entry is to be considered (1) or ignored (0). |
| 8 | Class | Indicates the type of object annotated |
| 9 | Visibility | Visibility ratio, a number between 0 and 1 that says how much of that object is visible. Can be due to occlusion and due to image border cropping. |

Classes of detected objects and their corresponding values:

| Class | ID |
|:-----:|:------:|
| Pedestrian | 1 |
| Person on vehicle| 2 |
| Car | 3 |
| Bicycle | 4 |
| Motorcycle | 5 |
| Non motorized vehicle | 6 |
| Static person | 7 |
| Distractor | 8 |
| Occluder | 9 |
| Occluder on the ground | 10 |
| Occluder full | 11 |
| Reflection | 12 |