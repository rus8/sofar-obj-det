"""Simple script to view bounding boxes on images.

Using converted labels from json draw bounding boxes on image and
view it.
"""

import cv2
import os
import json
import numpy as np
import random

# Colors for bounding boxes (! BGR)
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

# Paths to images folder and labels json file
images_path = '/home/rr/Desktop/Caltech-dataset/images'
labels_file = "/home/rr/Desktop/Caltech-dataset/caltech-labels.json"

# Load labels in dictionary
with open(labels_file, 'r') as fp:
    labels = json.load(fp)

# Get list of image files (would be randomly ordered as taken from dict)
frames = np.array(list(labels.keys()))

for frame_file in frames:
    file_dir = os.path.join(images_path, frame_file)
    img = cv2.imread(file_dir)

    for box in labels[frame_file]:
        color = random.choice(color_codes)
        x1 = round(box[0])
        y1 = round(box[1])
        x2 = round(box[2])
        y2 = round(box[3])
        font = cv2.FONT_HERSHEY_PLAIN
        img = cv2.rectangle(img, (x1, y1), (x2, y2), color, thickness=2)

    # Show resulting image
    cv2.imshow('Dataset sample', img)
    # Wait for user input
    k = cv2.waitKey(0)
    # Stop script if "ESC" button is pressed
    if k == 27:
        break

cv2.destroyWindow('Dataset sample')