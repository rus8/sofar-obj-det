from darkflow.net.build import TFNet
import cv2
import glob
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

darkflow_path = '/home/rr/git/darkflow/'

if __name__ == "__main__":

    options = {"model": darkflow_path+"cfg/tiny-yolo-voc.cfg", "load": darkflow_path+"bin/tiny-yolo-voc.weights", "threshold": 0.2}

    detector = TFNet(options)

    cap = cv2.VideoCapture(0)
    rval, frame = cap.read()

    while rval:
        img = frame
        # {'bottomright': {'x': 264, 'y': 213}, 'confidence': 0.3534133, 'label': 'car', 'topleft': {'x': 193, 'y': 174}}
        bboxes = detector.return_predict(img)
        for box in bboxes:
            if box['label'] == 'person':
                color = random.choice(color_codes)
                x1 = box['topleft']['x']
                y1 = box['topleft']['y']
                x2 = box['bottomright']['x']
                y2 = box['bottomright']['y']
                font = cv2.FONT_HERSHEY_PLAIN
                img = cv2.rectangle(img, (x1, y1), (x2, y2), color, thickness=2)
                img = cv2.putText(img, box['label'], (x1, y1), font, 1, color, thickness=2)


        cv2.imshow("Camera stream", img)
        rval, frame = cap.read()
        key = cv2.waitKey(10)
        # exit on ESC, you may want to uncomment the print to know which key is ESC for you
        if key == 27 or key == 1048603:
            break

    cv2.destroyWindow("Camera stream")
