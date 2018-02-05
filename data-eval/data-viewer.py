"""Simple script to view bounding boxes on images.

Using converted labels from json draw bounding boxes on image and
view it.
"""

import cv2
import os
import json
import numpy as np
import random

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

images_path = '/home/rr/Desktop/Caltech-dataset/images'

labels_file = "/home/rr/Desktop/Caltech-dataset/caltech-labels.json"

with open(labels_file, 'r') as fp:
    labels = json.load(fp)

frames = np.array(list(labels.keys()))
# rand_frames_inds = np.random.choice(len(frames), nb_samples)
for frame_file in frames: #[rand_frames_inds]:round
    file_dir = os.path.join(images_path, frame_file)
    img = cv2.imread(file_dir)
    # img = self.draw_data(frame_file)
    # img = self.draw_data(img, self.det_gt[frame_file])

    for box in labels[frame_file]:
        color = random.choice(color_codes)
        x1 = round(box[0])
        y1 = round(box[1])
        x2 = round(box[2])
        y2 = round(box[3])
        font = cv2.FONT_HERSHEY_PLAIN
        img = cv2.rectangle(img, (x1, y1), (x2, y2), color, thickness=2)

    cv2.imshow('Dataset sample', img)
    k = cv2.waitKey(0)
    if k == 27:
        cv2.destroyWindow('Dataset sample')
        break