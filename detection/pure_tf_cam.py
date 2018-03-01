""" Simple example of using "objdet"

Detects object in camera stream.
"""

import random
import cv2
import json
from objdet.pure_tf_detector import Detector

#! BGR
color_codes = [
    (0, 0, 255),  # red
    (0, 255, 0),  # lime
    (255, 0, 255),  # magenta
    (128, 0, 128),  # purple
    (0, 215, 255),  # gold
    (238, 130, 238),  # violet
    (0, 255, 255),  # yellow
    (0, 69, 255),  # orange red
    (127, 255, 0)  # spring green
]

net_files_path = 'built_graph/'

# Network file and metaparams file required to properly postprocess network output.
pb_file = net_files_path + 'tiny-yolo-voc.pb'
meta_file = net_files_path + 'tiny-yolo-voc.meta'

threshold = 0.5

if __name__ == "__main__":

    # Init the detector from files
    detector = Detector(pb_file, meta_file)

    cap = cv2.VideoCapture(0)
    rval, frame = cap.read()

    while rval:
        img = frame
        # Format of each bounding box in the list returned by return_predict() function.
        # {'bottomright': {'x': 264, 'y': 213}, 'confidence': 0.3534133, 'label': 'car', 'topleft': {'x': 193, 'y': 174}}
        bbs = detector.return_predict(img, threshold)
        res_dict = dict()
        i = 0
        for box in bbs:
            box['confidence'] = int(box['confidence']*100)  # Confidence in percents without decimals
            res_dict[str(i)] = box
            i += 1

        # Example of dict->string->dict conversion
        result = json.dumps(res_dict)  # Creating a string from dictionary (so it's possible to use in ROS)
        bboxes = json.loads(result)  # Parsing string back to dictionary

        # Drawing boxes
        for box in bboxes.values():
            color = random.choice(color_codes)
            x1 = box['topleft']['x']
            y1 = box['topleft']['y']
            x2 = box['bottomright']['x']
            y2 = box['bottomright']['y']
            font = cv2.FONT_HERSHEY_PLAIN
            img = cv2.rectangle(img, (x1, y1), (x2, y2), color, thickness=2)
            img = cv2.putText(img, box['label']+' '+str(box['confidence'])+' %', (x1, y1), font, 1, color, thickness=2)


        cv2.imshow("Camera stream", img)
        rval, frame = cap.read()
        key = cv2.waitKey(10)
        # exit on ESC, you may want to uncomment the print to know which key is ESC for you
        if key == 27 or key == 1048603:
            break

    cv2.destroyWindow("Camera stream")
