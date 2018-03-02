#!/usr/bin/env python

""" Example of using object detector

This node subscribes to topic with images and applies detector
to find objects. It publishes detected bounding boxes with a
time stamp of image using custom message type DetectedBoxes.
"""

import rospy
import cv2
import json
import random
# from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from objdet.pure_tf_detector import Detector
import std_msgs
from detect_msg.msg import DetectedBoxes

# BGR!
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

class ObjDetector:
    def __init__(self, camera_topic, detection_topic, pb_path, meta_path, threshold):
        """
        Initializes detector

        :param camera_topic: Name of topic to subscribe.
        """
        self.bridge = CvBridge()
        # self.image_sub = rospy.Subscriber(camera_topic, Image, self.callback)
        self.bboxes_pub = rospy.Publisher('my_camera_inference', DetectedBoxes, queue_size=5)

        self.bridge = CvBridge()

        self.detector = Detector(pb_path, meta_path)
        self.threshold = threshold

        rospy.init_node('cam_inf_pub')

    def cam_inference(self):
        rate = rospy.Rate(1)  # 1 Hz
        cap = cv2.VideoCapture(0)  # Init source of frames
        retv, img = cap.read()
        # While roscore is running and while camera is able to return frames
        while (not rospy.is_shutdown()) and retv:
            retv, img = cap.read()

            boxes_list = self.detector.return_predict(img, self.threshold)

            # Drawing boxes
            for box in boxes_list:
                color = random.choice(color_codes)
                x1 = box['topleft']['x']
                y1 = box['topleft']['y']
                x2 = box['bottomright']['x']
                y2 = box['bottomright']['y']
                font = cv2.FONT_HERSHEY_PLAIN
                img = cv2.rectangle(img, (x1, y1), (x2, y2), color, thickness=2)
                img = cv2.putText(img, box['label'] + ' ' + str(int(box['confidence'] * 100)) + ' %', (x1, y1), font, 1, color,
                                  thickness=2)

            cv2.imshow("Camera stream", img)
            cv2.waitKey(10)

            msg_to_pub = self.msg_constructor(boxes_list)
            self.bboxes_pub.publish(msg_to_pub)
            rate.sleep()

    def msg_constructor(self, boxes_list):
        """Construct DetectedBoxes message.

        :param boxes_list: List of predicted bounding boxes with labels.
        :return: DetectedBoxes message.
        """
        detect_msg = DetectedBoxes()
        detect_msg.header = std_msgs.msg.Header()
        detect_msg.header.stamp = rospy.Time.now()

        res_dict = dict()
        i = 0
        for box in boxes_list:
            box['confidence'] = int(box['confidence'] * 100)  # Confidence in percents without decimals
            res_dict[str(i)] = box
            i += 1

        detect_msg.dictionary = json.dumps(res_dict) # Creating a string from dictionary and put in msg field

        return detect_msg

if __name__ == "__main__":

    net_files_path = '/home/rr/Desktop/built_graph/'

    pb_file = net_files_path + 'tiny-yolo-voc.pb'
    meta_file = net_files_path + 'tiny-yolo-voc.meta'

    threshold = 0.5

    detector = ObjDetector("/my_camera_frame", "my_boxes", pb_file, meta_file, threshold)
    try:
        detector.cam_inference()
    except KeyboardInterrupt:
        print("Shutting down")
        cv2.destroyAllWindows()


